# OpenVSP reference parts

Selectable, self-contained OpenVSP components for geometry studies. For a new model on OpenVSP 3.57, check the native options first. Install individual files when you need their particular parameterization.

## Native geometry or a custom part?

| Geometry | In standard OpenVSP 3.57 | What the part adds |
| --- | --- | --- |
| Conical, tangent-ogive and secant-ogive noses | Stack or Fuselage end caps. The ogive angle controls tangency. | A separate component. `OgiveNosecone` sweeps from cone through non-bulging secants to the tangent ogive with one fraction. |
| Power-law nose | Power Law cap. The 3.57.1 Stack exponent control spans 0.05 to 20. | `PowerSeriesNosecone` covers the original 0 to 1 range, including very small exponents and the flat-ended cylinder at zero. |
| Haack-series nose | The Von Karman cap exposes Haack C. Its 3.57.1 range is 0 to 2/3, including LD-Haack (0) and LV-Haack (1/3). | `HaackSeriesNosecone` also covers the original range above 2/3 through 1, where the nose can grow wider than its base. New instances start at C = 0. |
| Full Sears–Haack body | The named cap is a half-body. A native Body of Revolution in Upper mode with a Super Ellipse section, width = full length, height = maximum diameter, M = 2, N = 4/3 and MaxWLoc = 0 gives the full mathematical meridian. | `SearsHaack` gives a two-ended body with direct length, maximum diameter and station count controls. The BOR is classified as a wing-type surface for thin-surface analyses. |
| Parabolic-series nose | No dedicated K′ end-cap control was found. The Power Law exponent of 1/2 gives a different meridian. | `ParabolicNosecone` sweeps the conventional family with one control, including the cone at K′ = 0 and the tangent-at-base full parabola at K′ = 1. |
| Elliptical nose | Ellipsoid supplies a full three-axis ellipsoid. A round cap on a straight circular body supplies a hemisphere at relative length 1. | `EllipticalNosecone` gives a flat-backed half-ellipsoid with independent axial length and diameter. |
| Other reference solids | Stack can make a frustum or a cylinder with round caps. BOR with Upper and Super Ellipse can make a superellipsoid of revolution. | `ConicalFrustum` uses two end diameters and a length. `Spherocylinder` uses barrel length and diameter, including the sphere at zero barrel length. `SuperellipsoidPod` ties the two meridional exponents to one control, from 1.5 to 6. |

The other ten original components are adaptations of the bundled OpenVSP examples. These are Box, BoxGroup, Cone, Disk, Duct, OnOffExample, PodMan, Seat, SeatGroup and TransportFuse. The revised versions retain their original filenames and parameter keys. The group seat layout accommodates empty seating blocks. The transport fuselage proportionally shortens the nose and tail if their requested lengths exceed the available space. The upstream agreement for the example scripts is in [licenses/OpenVSP-NOSA.txt](licenses/OpenVSP-NOSA.txt).

[OpenVSP 3.57 release notes](https://openvsp.org/blogs/announcements/2026/11/22/openvsp-3-57-0-released) · [Fuselage and Stack](https://openvsp.org/help_docs/latest/FuselageStack.html) · [Body of Revolution](https://openvsp.org/help_docs/latest/BOR.html) · [Cross Section Curves](https://openvsp.org/help_docs/latest/XSecCurves.html)

## Install

Copy the desired root-level `.vsppart` files into `%USERPROFILE%\CustomScripts` on Windows or `~/CustomScripts` on Linux or macOS. Restart OpenVSP, select the filename in the Geom Browser's component list and click **Add**. Set dimensions on **Design** in your model units.

OpenVSP searches the working directory, user home and installation directory in that order. A different script with the same name from a later directory gets a numeric suffix. A saved model embeds the script it used. To try a revised part in an older model, add a fresh component and transfer its settings. [OpenVSP custom-component guide](https://openvsp.org/help_docs/latest/Custom.html)

## Profile definitions

Let $u=x/L$ and $R=D/2$. Each nose runs from its tip at $x=0$ to a planar base at $L$. The legacy Cone has its base at $x=0$ and apex at its Height.

| Part | Meridian |
| --- | --- |
| SearsHaack | $r/R=[4u(1-u)]^{3/4}$. Its volume is $3\pi^2R^2L/16$. |
| EllipticalNosecone | $r/R=\sqrt{u(2-u)}$ |
| ParabolicNosecone | $r/R=(2u-K'u^2)/(2-K')$ |
| PowerSeriesNosecone | $r/R=u^N$ for $N>0$. At zero the part has two planar ends. |
| HaackSeriesNosecone | $r/R=\sqrt{(\theta-\sin(2\theta)/2+C\sin^3\theta)/\pi}$, where $\theta=\arccos(1-2u)$. |
| OgiveNosecone | A circular arc through the tip and base rim. Its half central angle is ArcFraction times $\arctan(R/L)$. Length/diameter is at least 0.5. |
| SuperellipsoidPod | $\lvert 2u-1\rvert^p+(r/R)^p=1$. At $p=2$ the body is a spheroid. |

The analytic curves define the stations and tangent directions. OpenVSP skins between them. The default station count is 35 on the adjustable profiles. Increasing **Cross sections** refines the loft. **Tess U/W** control the tessellation of that loft. A zero-exponent cylinder needs at least four sections, including both cap centers. [Profile equations, Appendix A](https://dept.aem.umn.edu/~./faculty/flaten/Rocketry_Remote_Lessons_Fall_2017/OpenRocketTechnicalDocumentationVersion13_05.pdf)

## Run the checks

From the checkout, supply the path to the OpenVSP script executable. Python uses only its standard library.

```powershell
python tests/run_checks.py "C:\OpenVSP\vspscript.exe"
```

The runner stages this checkout in a temporary working directory and fails on script errors or failed checks. It loads all 19 components, exercises design edits and scaling, and checks a saved model after reloading it. The profile tests query the actual skin at 601 longitudinal positions and three azimuths per case. They check surface residuals, section ordering, closure, planar bases, full-body symmetry and integrated Sears–Haack volume. The checks run headlessly with OpenVSP 3.57.1.
