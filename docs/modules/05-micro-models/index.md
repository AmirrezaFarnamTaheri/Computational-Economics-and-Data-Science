# Module 5: Microeconomic Models

Solve advanced microeconomic problems using computational methods.

---

## Overview

This module applies computational techniques to microeconomic theory, covering consumer and producer behavior, general equilibrium, game theory, discrete choice, and information economics. You'll learn to solve complex optimization problems and strategic interactions computationally.

**Duration:** 5-6 weeks
**Difficulty:** Advanced
**Prerequisites:** Modules 1-3, Intermediate Microeconomics

---

## Learning Objectives

By the end of this module, you will be able to:

- ✓ Solve consumer and producer optimization problems numerically
- ✓ Compute competitive and general equilibrium
- ✓ Analyze strategic games using computational methods
- ✓ Estimate and simulate discrete choice models
- ✓ Model principal-agent problems
- ✓ Solve information economics problems
- ✓ Apply auction theory computationally

---

## Topics Covered

### 1. Consumer and Producer Theory
**Notebook:** `01_Consumer_and_Producer_Theory.ipynb`

**Consumer Theory:**
- Utility maximization with budget constraints
- Expenditure minimization
- Demand systems (CES, translog, AIDS)
- Slutsky equations numerically
- Welfare analysis (compensating/equivalent variation)

**Producer Theory:**
- Cost minimization
- Profit maximization
- Production functions (Cobb-Douglas, CES, translog)
- Input demand and output supply
- Duality in production

**Computational Methods:**
- Constrained optimization
- Numerical comparative statics
- Elasticity computation

**Applications:**
- Tax incidence analysis
- Price changes and welfare
- Technology adoption

---

### 2. General Equilibrium
**Notebook:** `02_General_Equilibrium.ipynb`

- Walrasian equilibrium computation
- Excess demand functions
- Market-clearing algorithms
- Existence and uniqueness issues
- Computable General Equilibrium (CGE) models
- Multi-sector economies

**Solution Techniques:**
- Fixed-point algorithms (Scarf, Merrill)
- Newton methods for market clearing
- Homotopy continuation
- Negishi approach

**Applications:**
- Trade policy analysis
- Tax reform evaluation
- Environmental policy
- Distributional effects

---

### 3. Game Theory and Auctions
**Notebook:** `03_Game_Theory_and_Auctions.ipynb`

**Game Theory:**
- Nash equilibrium computation
- Repeated games and folk theorems
- Dynamic games and subgame perfection
- Bayesian games
- Mechanism design

**Auction Theory:**
- First-price sealed-bid auctions
- Second-price (Vickrey) auctions
- English and Dutch auctions
- Revenue equivalence
- Optimal auction design

**Computational Methods:**
- Best-response iteration
- Support enumeration
- Lemke-Howson algorithm
- Monte Carlo simulation of games

**Applications:**
- Oligopoly competition
- Spectrum auctions
- Procurement design
- Collusion detection

---

### 4. Discrete Choice Models
**Notebook:** `04_Discrete_Choice_Models.ipynb`

- Binary choice (logit, probit)
- Multinomial logit and nested logit
- Mixed logit (random coefficients)
- Conditional logit
- Independence of Irrelevant Alternatives (IIA)
- Simulated maximum likelihood

**Computational Techniques:**
- Maximum likelihood estimation
- Simulation-based inference
- Importance sampling
- Halton sequences for Monte Carlo

**Applications:**
- Transportation mode choice
- Product differentiation
- Labor force participation
- Location choice

---

### 5. Principal-Agent Models
**Notebook:** `05_Principal_Agent_Models.ipynb`

- Hidden action (moral hazard)
- Hidden information (adverse selection)
- Screening and signaling
- Optimal contracts under asymmetric information
- Dynamic contracting
- Multi-agent problems

**Solution Methods:**
- Solving incentive compatibility constraints
- Participation constraints
- Revelation principle applications
- Numerical contract optimization

**Applications:**
- Labor contracts and compensation
- Insurance markets
- Financial intermediation
- Regulatory design

---

### 6. Information Economics
**Notebook:** `06_Information_Economics.ipynb`

- Signaling games (Spence model)
- Screening models (Rothschild-Stiglitz)
- Search and matching
- Information aggregation
- Learning and updating
- Reputation models

**Computational Challenges:**
- Solving for separating/pooling equilibria
- Multiple equilibria handling
- Stability and refinements
- Belief updating

**Applications:**
- Education as signal
- Credit markets with asymmetric information
- Job market signaling
- Market design with private information

---

## Prerequisites

### Required Knowledge

**Economics:**
- **Essential**: Intermediate microeconomics (consumer/producer theory, basic game theory)
- **Helpful**: Graduate micro (general equilibrium, contract theory)

**Mathematics:**
- Constrained optimization (Lagrange, Kuhn-Tucker)
- Probability theory
- Game theory basics
- Real analysis

**Programming:**
- Modules 1-3 completed
- Optimization proficiency
- Dynamic programming experience

---

## Key Libraries

- **SciPy**: Optimization (scipy.optimize)
- **NumPy**: Numerical operations
- **Statsmodels**: Discrete choice estimation
- **PyLogit/Biogeme**: Specialized choice modeling
- **Nashpy**: Game theory computations
- **Matplotlib/Seaborn**: Visualization

---

## Learning Path

### Week 1: Consumer and Producer
- Complete notebook 01
- Master duality concepts
- Compute demand systems

### Week 2: General Equilibrium
- Complete notebook 02
- Solve for market-clearing prices
- Build simple CGE models

### Week 3: Game Theory and Auctions
- Complete notebook 03
- Compute Nash equilibria
- Simulate auction mechanisms

### Week 4: Discrete Choice
- Complete notebook 04
- Estimate logit models
- Implement mixed logit

### Week 5: Principal-Agent
- Complete notebook 05
- Solve optimal contracts
- Handle moral hazard

### Week 6: Information Economics
- Complete notebook 06
- Analyze signaling equilibria
- Model adverse selection

---

## Practice Exercises

Key exercises throughout the module:

1. **Tax Incidence**: Compute welfare effects of commodity taxes
2. **Trade Liberalization**: CGE analysis of tariff removal
3. **Cournot Oligopoly**: Find Nash equilibrium numerically
4. **Auction Simulation**: Compare revenue across auction formats
5. **Choice Modeling**: Estimate discrete choice model with real data
6. **Optimal Contract**: Design incentive-compatible wage scheme
7. **Lemon's Market**: Solve Akerlof's adverse selection problem

---

## Computational Challenges

### Challenge: Multiple Equilibria
**Solutions:**
- Try multiple initial values
- Use homotopy/continuation methods
- Apply equilibrium selection criteria
- Document all equilibria found

### Challenge: High-Dimensional Optimization
**Solutions:**
- Exploit problem structure (separability)
- Use gradient information
- Apply global optimization methods
- Consider approximation techniques

### Challenge: Simulation-Based Estimation
**Solutions:**
- Use quasi-random sequences (Halton, Sobol)
- Implement importance sampling
- Apply variance reduction techniques
- Parallelize simulations

---

## Real-World Applications

These methods are used in:

**Antitrust Analysis:**
- Merger simulations
- Market power assessment
- Collusion detection

**Public Policy:**
- Tax policy design
- Environmental regulation
- Healthcare reform
- Education policy

**Industry:**
- Pricing strategies
- Product design
- Market entry decisions
- Contract design

**Academic Research:**
- Industrial organization
- Labor economics
- Public economics
- Development economics

---

## Key Concepts and Techniques

### Duality Theory
- Primal and dual problems
- Envelope theorems
- Roy's identity and Shephard's lemma
- Hotelling's lemma

### Equilibrium Concepts
- Walrasian equilibrium
- Nash equilibrium
- Perfect Bayesian equilibrium
- Sequential equilibrium

### Mechanism Design
- Revelation principle
- Incentive compatibility
- Individual rationality
- Revenue equivalence

---

## Resources

### Essential Reading

**Textbooks:**
- Mas-Colell, A., Whinston, M., & Green, J. (1995). *Microeconomic Theory*
- Varian, H. (1992). *Microeconomic Analysis*, 3rd ed.
- Fudenberg, D. & Tirole, J. (1991). *Game Theory*
- Train, K. (2009). *Discrete Choice Methods with Simulation*

**Classic Papers:**
- Scarf, H. (1967). "On the Computation of Equilibrium Prices"
- McFadden, D. (1974). "Conditional Logit Analysis of Qualitative Choice Behavior"
- Spence, M. (1973). "Job Market Signaling"
- Myerson, R. (1981). "Optimal Auction Design"

### Software and Tools
- [Nashpy](https://nashpy.readthedocs.io/) - Game theory in Python
- [PyLogit](https://github.com/timothyb0912/pylogit) - Discrete choice models
- [GAMS](https://www.gams.com/) - General Algebraic Modeling System (CGE)

---

## Policy Applications

Learn to analyze:

- **Merger Effects**: Simulate post-merger equilibrium
- **Tax Policy**: Deadweight loss and incidence
- **Auction Design**: Revenue-maximizing mechanisms
- **Regulation**: Optimal regulatory contracts
- **Market Failures**: Information asymmetry solutions

---

## Assessment

To master this module, you should:

- [ ] Solve consumer/producer problems numerically
- [ ] Compute general equilibrium
- [ ] Find Nash equilibria in games
- [ ] Estimate discrete choice models
- [ ] Design optimal contracts
- [ ] Analyze signaling and screening
- [ ] Apply methods to policy questions

---

## Next Steps

After completing this module:

1. **Module 6: Econometrics** - Estimate micro models with data
2. **Module 7: Machine Learning** - Advanced choice modeling
3. **Module 4: Macro Models** - Combine micro and macro

---

## Tips for Success

1. **Economic Intuition First**: Understand the economic problem before coding
2. **Check Optimality**: Verify FOCs and constraint qualifications
3. **Multiple Initializations**: Try different starting points for equilibria
4. **Visualize**: Plot reaction functions, indifference curves, contract curves
5. **Validate**: Compare to analytical solutions when available

---

## Common Pitfalls

### Pitfall: Ignoring Constraint Qualifications
**Solution**: Always check if Kuhn-Tucker conditions apply

### Pitfall: Missing Equilibria
**Solution**: Use multiple random starting points

### Pitfall: IIA Assumption in Logit
**Solution**: Use nested or mixed logit for flexible substitution patterns

---

## Need Help?

- Review [Optimization](../02-numerical-methods/index.md#5-optimization)
- Check [Dynamic Programming](../03-economic-modeling/index.md)
- See [FAQ](../../resources/faq.md)
- Join [Discussions](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/discussions)

---

**Ready to dive into micro models?** Start with `01_Consumer_and_Producer_Theory.ipynb`!
