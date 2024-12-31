# FTDrawer

![LGPL-3.0 license](https://img.shields.io/badge/license-LGPL--3.0-red)

This application was created for calculating the Fourier coefficients of the complex function specifying 
the **first** path in the **SVG** file. 

And further displaying the first **n** terms of this series.

![example](example.png)

# Usage

```
python main.py [filename] [n] [f1]
```

n - number of terms: [-n, ..., 0, ..., n] terms.

f1 - carrier frequency

# Interaction

You can move camera with WASD or mouse buttons.

Also you can zoom with q/e or mouse wheel.

You can immediately close application by pressing ESC.

Keys and some other constants may be changed in config.py.