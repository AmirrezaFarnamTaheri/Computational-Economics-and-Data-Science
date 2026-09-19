#!/usr/bin/env python3
"""Rendered browser regressions for the published course site.

This suite complements the static notebook/docs audits. It exercises the built
MkDocs output in Chromium at desktop and narrow viewports, with WebGL disabled
and reduced motion enabled where relevant. The interactive lab is deliberately
Canvas 2D, so it must remain usable without WebGL.
"""

from __future__ import annotations

import argparse
import json
import socket
import subprocess
import sys
import time
import urllib.request
from contextlib import closing
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def free_port() -> int:
    """Return an available local TCP port."""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def wait_for_server(url: str, timeout: float = 15.0) -> None:
    """Wait until the local static server accepts requests."""
    deadline = time.monotonic() + timeout
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=1) as response:
                if response.status == 200:
                    return
        except Exception as exc:  # local startup race; report final cause below
            last_error = exc
        time.sleep(0.1)
    raise RuntimeError(f"Local docs server did not start: {last_error}")


def assert_no_horizontal_overflow(page: Page) -> None:
    """Require the rendered page to fit the viewport horizontally."""
    overflow = page.evaluate(
        "() => document.documentElement.scrollWidth - window.innerWidth"
    )
    if overflow > 1:
        offenders = page.evaluate("""() => [...document.querySelectorAll('body *')]
                .map((el) => {
                    const rect = el.getBoundingClientRect();
                    return {
                        tag: el.tagName.toLowerCase(),
                        id: el.id || '',
                        classes: typeof el.className === 'string' ? el.className : '',
                        left: Math.round(rect.left),
                        right: Math.round(rect.right),
                        width: Math.round(rect.width),
                    };
                })
                .filter((item) => item.right > window.innerWidth + 1 || item.left < -1)
                .sort((a, b) => (b.right - window.innerWidth) - (a.right - window.innerWidth))
                .slice(0, 12)""")
        raise AssertionError(
            f"horizontal overflow is {overflow}px; top offenders: {offenders}"
        )


def check_optimization_layout(page: Page, output_dir: Path) -> dict[str, object]:
    """Check the historical figure/caption block at desktop and mobile sizes."""
    page.goto(
        "/notebooks/02-Numerical-Methods/05_Optimization/",
        wait_until="domcontentloaded",
    )
    page.locator("figure.course-figure.course-portrait").first.wait_for()

    figure = page.locator("figure.course-figure.course-portrait").first
    caption = figure.locator("figcaption")
    assert caption.count() == 1, "historical figure must have exactly one figcaption"

    figure_box = figure.bounding_box()
    caption_box = caption.bounding_box()
    assert figure_box is not None and caption_box is not None
    assert figure_box["width"] <= 322, f"portrait width is {figure_box['width']}px"

    image = figure.locator("img")
    if image.count():
        image_box = image.bounding_box()
        assert image_box is not None
        assert (
            caption_box["y"] + 0.5 >= image_box["y"] + image_box["height"]
        ), "caption overlaps or sits beside the historical image"
        image_state = "published"
    else:
        # Unverified historical assets are intentionally replaced by the
        # provenance gate. The caption must still remain a separate block.
        blocked = figure.locator(".figure-provenance-blocked")
        assert blocked.count() == 1, "missing image must be provenance-gated"
        blocked_box = blocked.bounding_box()
        assert blocked_box is not None
        assert caption_box["y"] + 0.5 >= blocked_box["y"] + blocked_box["height"]
        image_state = "provenance-gated"

    output_dir.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=output_dir / "optimization-desktop.png", full_page=True)

    page.set_viewport_size({"width": 390, "height": 844})
    page.reload(wait_until="domcontentloaded")
    page.locator("figure.course-figure.course-portrait").first.wait_for()
    assert_no_horizontal_overflow(page)
    mobile_box = page.locator(
        "figure.course-figure.course-portrait"
    ).first.bounding_box()
    assert mobile_box is not None
    assert mobile_box["width"] <= 358, "portrait overflows the mobile content column"
    page.screenshot(path=output_dir / "optimization-mobile.png", full_page=True)

    return {
        "figure_width_desktop": round(figure_box["width"], 2),
        "figure_width_mobile": round(mobile_box["width"], 2),
        "image_state": image_state,
    }


def check_interactive_lab(page: Page, output_dir: Path) -> dict[str, object]:
    """Exercise responsive controls and deterministic Canvas 2D rendering."""
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto("/resources/interactive/", wait_until="domcontentloaded")
    page.locator("#surface-canvas").wait_for()
    assert_no_horizontal_overflow(page)

    canvas_checks = page.evaluate(
        """() => [...document.querySelectorAll('canvas')].map((canvas) => {
            const rect = canvas.getBoundingClientRect();
            const parent = canvas.parentElement.getBoundingClientRect();
            return {
                id: canvas.id,
                width: rect.width,
                parentWidth: parent.width,
                right: rect.right,
                viewport: window.innerWidth,
            };
        })"""
    )
    for item in canvas_checks:
        assert item["width"] <= item["parentWidth"] + 1
        assert item["right"] <= item["viewport"] + 1

    alpha = page.locator("#alpha-slider")
    alpha_output = page.locator("#alpha-value")
    before = page.locator("#surface-canvas").evaluate("(el) => el.toDataURL()")
    alpha.evaluate("""el => {
            el.value = '0.60';
            el.dispatchEvent(new Event('input', { bubbles: true }));
        }""")
    assert alpha_output.evaluate("(el) => el.value") == "0.60"
    after = page.locator("#surface-canvas").evaluate("(el) => el.toDataURL()")
    assert before != after, "surface canvas did not redraw after alpha changed"

    # Labels must be programmatically connected to every range input.
    unlabeled = page.evaluate(
        """() => [...document.querySelectorAll('input[type="range"]')]
            .filter((el) => !document.querySelector('label[for="' + el.id + '"]'))
            .map((el) => el.id)"""
    )
    assert unlabeled == [], f"unlabeled range controls: {unlabeled}"

    page.screenshot(path=output_dir / "interactive-mobile.png", full_page=True)
    return {"canvases": canvas_checks, "alpha_redraw": True}


def check_reduced_motion(page: Page) -> dict[str, object]:
    """Verify reduced-motion and no-WebGL operation leave controls usable."""
    page.goto("/resources/interactive/", wait_until="domcontentloaded")
    page.locator("#market-reset").wait_for()
    page.locator("#market-reset").click()
    assert page.locator("#market-trades").inner_text() == "0"

    # With reduced motion active, the market animation is intentionally not
    # scheduled. Controls and the static canvas must still be present.
    canvas_pixels = page.locator("#market-canvas").evaluate(
        "(el) => el.toDataURL().length"
    )
    assert canvas_pixels > 100
    return {"market_reset_works": True, "canvas_data_url_length": canvas_pixels}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-dir", type=Path, default=ROOT / "site")
    parser.add_argument(
        "--output-dir", type=Path, default=ROOT / "build" / "browser-regression"
    )
    args = parser.parse_args()

    site_dir = args.site_dir.resolve()
    if not (site_dir / "index.html").is_file():
        raise SystemExit(
            f"Built site not found at {site_dir}. Run 'mkdocs build --strict' first."
        )

    port = free_port()
    base_url = f"http://127.0.0.1:{port}"
    server = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "http.server",
            str(port),
            "--bind",
            "127.0.0.1",
            "--directory",
            str(site_dir),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    report: dict[str, object] = {"base_url": base_url}
    try:
        wait_for_server(base_url)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=True,
                args=["--disable-webgl", "--disable-gpu"],
            )
            try:
                context = browser.new_context(
                    base_url=base_url,
                    viewport={"width": 1280, "height": 900},
                )
                page = context.new_page()
                page_errors: list[str] = []
                page.on("pageerror", lambda error: page_errors.append(str(error)))
                report["optimization"] = check_optimization_layout(
                    page, args.output_dir
                )
                report["interactive"] = check_interactive_lab(page, args.output_dir)
                assert not page_errors, f"browser page errors: {page_errors}"
                context.close()

                reduced = browser.new_context(
                    base_url=base_url,
                    viewport={"width": 390, "height": 844},
                    reduced_motion="reduce",
                )
                reduced_page = reduced.new_page()
                reduced_errors: list[str] = []
                reduced_page.on(
                    "pageerror", lambda error: reduced_errors.append(str(error))
                )
                report["reduced_motion"] = check_reduced_motion(reduced_page)
                assert (
                    not reduced_errors
                ), f"reduced-motion page errors: {reduced_errors}"
                reduced.close()
            finally:
                browser.close()
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    report_path = args.output_dir / "report.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Browser regression passed; report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
