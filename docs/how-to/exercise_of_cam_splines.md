Ronald G. Mosier splines


EXAMPLE 5-1 Using a Classical Spline for a Single-Dwell Cam.

Problem:

Consider the following single - dwell cam specification:

| phase     | requirement                               |
| --------- | ----------------------------------------- |
| rise      | 1 inch(25.4 mm) in 90°                    |
| fall      | 1 inch(25.4 mm) in 90°                    |
| dwell     | at zero displacement for 180° (low dwell) |
| cam omega | 15 rad/sec                                |

Solution:

Table 5-2 Knot Locations and Boundary Conditions for 1st Try, Example 5-1

| Function     |  0   |  45  |  90  | 135  | 180  |
| ------------ | :--: | :--: | :--: | :--: | :--: |
| Displacement |  0   | 0.5  |  1   | 0.5  |  0   |
| Velocity     |  0   |  -   |  -   |  -   |  0   |
| Acceleration |  0   |  -   |  -   |  -   |  0   |




$$
\begin{cases} 0 & \text{for}\: x < 0 \\1.0009 x^{5} - 3.2265 x^{4} + 2.9487 x^{3} & \text{for}\: x \leq \frac{\pi}{4} \\1.1084 x - 0.1942 \left(x - \frac{\pi}{4}\right)^{5} + 0.704 \left(x - \frac{\pi}{4}\right)^{4} - 1.0136 \left(x - \frac{\pi}{4}\right)^{3} - 0.1447 \left(x - \frac{\pi}{4}\right)^{2} - 0.2771 \pi + 0.5 & \text{for}\: x \leq \frac{\pi}{2} \\0.1942 \left(x - \frac{\pi}{2}\right)^{5} - 0.0587 \left(x - \frac{\pi}{2}\right)^{4} - 0.8685 \left(x - \frac{\pi}{2}\right)^{2} + 1.0 & \text{for}\: x \leq \frac{3 \pi}{4} \\- 1.1084 x - 1.0009 \left(x - \frac{3 \pi}{4}\right)^{5} + 0.704 \left(x - \frac{3 \pi}{4}\right)^{4} + 1.0136 \left(x - \frac{3 \pi}{4}\right)^{3} - 0.1447 \left(x - \frac{3 \pi}{4}\right)^{2} + 0.5 + 0.8313 \pi & \text{for}\: x \leq \pi \\0 & \text{otherwise} \end{cases}
$$
v
$$
\begin{cases} 0 & \text{for}\: x < 0 \\5.0045 x^{4} - 12.906 x^{3} + 8.8461 x^{2} & \text{for}\: x \leq \frac{\pi}{4} \\- 0.2894 x - 0.971 \left(x - \frac{\pi}{4}\right)^{4} + 2.816 \left(x - \frac{\pi}{4}\right)^{3} - 3.0408 \left(x - \frac{\pi}{4}\right)^{2} + 0.07235 \pi + 1.1084 & \text{for}\: x \leq \frac{\pi}{2} \\- 1.737 x + 0.971 \left(x - \frac{\pi}{2}\right)^{4} - 0.2348 \left(x - \frac{\pi}{2}\right)^{3} + 0.8685 \pi & \text{for}\: x \leq \frac{3 \pi}{4} \\- 0.2894 x - 5.0045 \left(x - \frac{3 \pi}{4}\right)^{4} + 2.816 \left(x - \frac{3 \pi}{4}\right)^{3} + 3.0408 \left(x - \frac{3 \pi}{4}\right)^{2} - 1.1084 + 0.21705 \pi & \text{for}\: x \leq \pi \\0 & \text{otherwise} \end{cases}
$$
