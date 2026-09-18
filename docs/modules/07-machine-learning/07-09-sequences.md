# CNNs & RNNs

> This page is synchronized from the authoritative notebooks. Use the generated reading view for searchable prose/code, or open the notebook for execution.

## 07 Convolutional Neural Networks

**What problem are we solving?** Images and spatial data (satellite imagery, maps, heatmaps) contain rich economic information. Standard neural networks ignore spatial structure. **CNNs** exploit local connectivity and translation invariance to efficiently learn spatial features. **Why this method?** Economists increasingly use satellite imagery to measure poverty, urbanization, and agricultural output. CNNs are the 

[Read generated page](../../notebooks/07-Machine-Learning/07_Convolutional_Neural_Networks.md){ .md-button } [Open notebook](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/blob/main/07-Machine-Learning/07_Convolutional_Neural_Networks.ipynb){ .md-button }

## 08 Recurrent Neural Networks

**What problem are we solving?** Economic time series and text are sequential: the order of observations matters. Standard feedforward networks treat inputs as unordered. **RNNs** maintain a hidden state that evolves over time, capturing temporal dependencies. **Why this method?** RNNs are foundational for sequence modeling tasks: forecasting GDP, modeling language in central bank communications, and processing varia

[Read generated page](../../notebooks/07-Machine-Learning/08_Recurrent_Neural_Networks.md){ .md-button } [Open notebook](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/blob/main/07-Machine-Learning/08_Recurrent_Neural_Networks.ipynb){ .md-button }

## 09 LSTMs and GRUs

**What problem are we solving?** Vanilla RNNs struggle to learn dependencies over long sequences (vanishing gradients). **LSTMs** and **GRUs** introduce gating mechanisms that selectively remember or forget information, enabling learning over hundreds of time steps. **Why this method?** LSTMs are the workhorse for economic sequence tasks: forecasting financial volatility, modeling consumption paths, and analyzing tex

[Read generated page](../../notebooks/07-Machine-Learning/09_LSTMs_and_GRUs.md){ .md-button } [Open notebook](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/blob/main/07-Machine-Learning/09_LSTMs_and_GRUs.ipynb){ .md-button }
