lh_pit = r"""
\begin{equation}
    h_{LH_{pit}}(E2, P4, G\mhyphen R, LH_{pit}) = (b^{LH}_{syn}+k^{LH}_{E2} * X_{E2}) * (1-X_{P4}) \\ -(b^{LH}_{Rel}+k^{LH}_{G\mhyphen R} * X_{G\mhyphen R}) * X_{LH_{pit}}
\end{equation}
"""

lh_blood = r"""
\begin{equation}
    h_{LH_{blood}}(G\mhyphen R, LH_{pit}, R_{LH}, LH_{blood}) = \frac{1}{V_{blood}} * (b^{LH}_{Rel}+k^{LH}_{G\mhyphen R} * X_{G\mhyphen R}) * X_{LH_{pit}} \\ -(k^{LH}_{on} * X_{R_{LH}}+k^{LH}_{cl}) * X_{LH_{blood}}
\end{equation}
"""

fsh_pit = r"""
\begin{equation}
    h_{FSH_{pit}}(IhA_{e}, IhB, freq, G\mhyphen R, FSH_{pit}) \\ = (1-X_{IhA_{e}}) * (1-X_{IhB}) * (1-X_{freq}) \\ - (b^{FSH}_{Rel}+k^{FSH}_{G\mhyphen R} * X_{G\mhyphen R}) * X_{FSH_{pit}}
\end{equation}
"""

fsh_blood = r"""
\begin{equation}
    h_{FSH_{blood}}(G\mhyphen R, FSH_{pit}, R_{FSH}, FSH_{blood}) \\ = \frac{1}{V_{blood}} * (b^{FSH}_{Rel}+k^{FSH}_{G\mhyphen R} * X_{G\mhyphen R}) * X_{FSH_{pit}} \\ - (k^{FSH}_{on} * X_{R_{FSH}} + k^{FSH}_{cl}) * X_{FSH_{blood}}
\end{equation}
"""

rfsh = r"""
\begin{equation}
    h_{R_{FSH}}(R_{FSH,des}, FSH_{blood}, R_{FSH}) \\ = k^{FSH}_{recy} * X_{R_{FSH,des}} - k^{FSH}_{on} * X_{FSH_{blood}} * X_{R_{FSH}}
\end{equation}
"""

fshr = r"""
\begin{equation}
    h_{FSH\mhyphen R}(FSH_{blood}, R_{FSH}, FSH\mhyphen R) \\ = k^{FSH}_{on} * X_{FSH_{blood}} * X_{R_{FSH}} - k^{FSH}_{des} * X_{FSH\mhyphen R}
\end{equation}
"""

rfshdes = r"""
\begin{equation}
    k_{R_{FSH,des}}(FSH\mhyphen R, R_{FSH,des}) \\ = k^{FSH}_{des} * X_{FSH\mhyphen R} - k^{FSH}_{recy} * X_{R_{FSH,des}}
\end{equation}
"""

rlh = r"""
\begin{equation}
    h_{R_{LH}}(R_{LH,des}, LH_{blood}, R_{LH}) \\ = k^{LH}_{recy} * X_{R_{LH,des}} - k^{LH}_{on} * X_{LH_{blood}} * X_{R_{LH}}
\end{equation}
"""

lhr = r"""
\begin{equation}
    h_{LH\mhyphen R}(LH_{blood}, R_{LH}, LH\mhyphen R) \\ = k^{LH}_{on} * X_{LH_{blood}} * X_{R_{LH}} - k^{LH}_{des} * X_{LH\mhyphen R}
\end{equation}
"""

rlhdes = r"""
\begin{equation}
    h_{R_{LH,des}}(LH\mhyphen R, R_{LH,des}) = k^{LH}_{des} * X_{LH\mhyphen R} - k^{LH}_{recy} * X_{R_{LH,des}}
\end{equation}
"""

eqs = r"""
\begin{equation}
    h_{s}(FSH_{blood}, P4, s) = k^{s} * X_{FSH_{blood}} - k^{s}_{cl} * X_{P4} * X_{s}
\end{equation}
"""

af1 = r"""
\begin{equation}
    h_{AF1}(FSH\mhyphen R, AF1) \\ = K^{AF1} * X_{FSH\mhyphen R} - k^{AF2}_{AF1} * X_{FSH\mhyphen R} * X_{AF1}
\end{equation}
"""

af2 = r"""
\begin{equation}
    h_{AF2}(FSH\mhyphen R, AF1, LH\mhyphen R, s, AF2) \\ = k^{AF2}_{AF1} * X_{FSH\mhyphen R} * X_{AF1} - k^{AF3}_{AF2} * \frac{X_{LH\mhyphen R}}{SF_{LH}R} * X_{s} * X_{AF2}
\end{equation}
"""

af3 = r"""
\begin{equation}
    h_{AF3}(LH\mhyphen R, s, AF2, FSH\mhyphen R, AF3) \\ =  k^{AF3}_{AF2} * \frac{X_{LH\mhyphen R}}{SF_{LH}R} * X_{s} * X_{AF2} \\ + k^{AF3}_{AF3} * X_{FSH\mhyphen R} * X_{AF3} *(1-\frac{X_{AF3}}{SeF_{max}}) \\ - k^{AF4}_{AF3} * \frac{X_{LH\mhyphen R}}{SF_{LH}R} * X_{s} * X_{AF3}
\end{equation}
"""

af4 = r"""
\begin{equation}
    h_{AF4}(LH\mhyphen R, s, AF3, AF4) \\ = k^{AF4}_{AF3} * \frac{X_{LH\mhyphen R}}{SF_{LH}R} * X_{s} * X_{AF3} \\ + k^{AF4}_{AF4} * \frac{X_{LH\mhyphen R}}{SF_{LH}R} * X_{AF4} * (1-\frac{X_{AF4}}{SeF_{max}}) \\ - k^{PrF}_{AF4} * \frac{X_{LH\mhyphen R}}{SF_{LH}R} * X_{s} * X_{AF4}
\end{equation}
"""

prf = r"""
\begin{equation}
    h_{PrF}(LH\mhyphen R, s, AF4, PrF) \\ = k^{PrF}_{AF4} * \frac{X_{LH\mhyphen R}}{SF_{LH}R} * X_{s} * X_{AF4} \\ - k^{PrF}_{cl} * \frac{X_{LH\mhyphen R}}{SF_{LH}R} * X_{s} * X_{PrF}
\end{equation}
"""

ovf = r"""
\begin{equation}
    h_{OvF}(LH\mhyphen R, s, PrF, OvF) \\ = k^{OvF} * \frac{X_{LH\mhyphen R}}{SF_{LH}R} * X_{s} * X_{PrF} - k^{OvF}_{cl} * X_{OvF}
\end{equation}
"""

sc1 = r"""
\begin{equation}
    h_{Sc1}(OvF, Sc1) = k^{Sc1} * X_{OvF} - k^{Sc2}_{Sc1} * X_{Sc1}
\end{equation}
"""

sc2 = r"""
\begin{equation}
    h_{Sc2}(Sc1, Sc2) = k^{Sc2}_{Sc1} * X_{Sc1} - k^{Lut1}_{Sc2} * X_{Sc2}
\end{equation}
"""

lut1 = r"""
\begin{equation}
    h_{Lut1}(Sc2, G\mhyphen R_{a}, Lut1) \\ = k^{Lut1}_{Sc2} * X_{Sc2} - k^{Lut2}_{Lut1} * (1+m^{Lut}_{G\mhyphen R} * X_{G\mhyphen R_{a}})*X_{Lut1}
\end{equation}
"""

lut2 = r"""
\begin{equation}
    h_{Lut2}(G\mhyphen R_{a}, Lut1, Lut2) \\ = k^{Lut2}_{Lut1} * (1+m^{Lut}_{G\mhyphen R} * X_{G\mhyphen R_{a}})*X_{Lut1} \\ - k^{Lut3}_{Lut2} * (1+m^{Lut}_{G\mhyphen R} * X_{G\mhyphen R_{a}})*X_{Lut2}
\end{equation}
"""

lut3 = r"""
\begin{equation}
    h_{Lut3}(G\mhyphen R_{a}, Lut2, Lut3) \\ = k^{Lut3}_{Lut2} * (1+m^{Lut}_{G\mhyphen R} * X_{G\mhyphen R_{a}})*X_{Lut2} \\ - k^{Lut4}_{Lut3} * (1+m^{Lut}_{G\mhyphen R} * X_{G\mhyphen R_{a}})*X_{Lut3}
\end{equation}
"""

lut4 = r"""
\begin{equation}
    h_{Lut4}(G\mhyphen R_{a}, Lut3, Lut4) \\ = k^{Lut4}_{Lut3} * (1+m^{Lut}_{G\mhyphen R} * X_{G\mhyphen R_{a}})*X_{Lut3} \\ - k^{Lut4}_{cl} * (1+m^{Lut}_{G\mhyphen R} * X_{G\mhyphen R_{a}})*X_{Lut4}
\end{equation}
"""

e2 = r"""
\begin{equation}
    h_{E2}(AF2, AF3, AF4, LH_{blood}, PrF, Lut1, Lut4, E2) \\ = b^{E2} + k^{E2}_{AF2} * X_{AF2} + k^{E2}_{AF3} * X_{LH_{blood}} * X_{AF3} + k^{E2}_{AF4} * X_{AF4} + k^{E2}_{Prf} * X_{LH_{blood}} * X_{PrF} + k^{E2}_{Lut1} * X_{Lut1} + k^{E2}_{Lut4} * X_{Lut4} - k^{E2}_{cl} * X_{E2}
\end{equation}
"""

p4 = r"""
\begin{equation}
    h_{P4}(Lut4, P4) \\ = b^{P4} + k^{P4}_{Lut4} * X_{Lut4} - k^{P4}_{cl} * X_{P4}
\end{equation}
"""

iha = r"""
\begin{equation}
    h_{IhA}(PrF, Sc1, Lut1, Lut2, Lut3, Lut4, IhA) \\ = b^{IhA} + k^{IhA}_{PrF} * X_{PrF} + k^{IhA}_{Sc1}*X_{Sc1} + k^{IhA}_{Lut1} * X_{Lut1} + k^{IhA}_{Lut2} * X_{Lut2} + k^{IhA}_{Lut3} * X_{Lut3} + k^{IhA}_{Lut4} * X_{Lut4} - k^{IhA} * X_{IhA}
\end{equation}
"""

ihb = r"""
\begin{equation}
    h_{IhB}(AF2, Sc2, IhB) \\ = b^{IhB} + k^{IhB}_{AF2} * X_{AF2} + k^{IhB}_{SC2} * X_{Sc2} - k^{IhB}_{cl} * X_{IhB}
\end{equation}
"""

ihae = r"""
\begin{equation}
    h_{IhA_{e}}(IhA, IhA_{e}) \\ = k^{IhA} * X_{IhA} - k^{IhA_{e}}_{cl} * X_{IhA_{e}}
\end{equation}
"""

freq = r"""
\begin{equation}
    freq(P4, E2) = f_{0} * (1-X_{P4}) * (1 + m^{freq}_{E2} * X_{E2})
\end{equation}
"""

mass = r"""
\begin{equation}
    mass(E2) \\ = alpha_{0} * X_{E2} + (1-X_{E2})
\end{equation}
"""

gnrh = r"""
\begin{equation}
    h_{GnRH}(mass, freq, GnRH, R_{G,a}, G\mhyphen R_{a}) \\ = X_{mass} * X_{freq} - k^{GnRH}_{on} * X_{GnRH} * X_{R_{G,a}} + k^{GnRH}_{off} * X_{G\mhyphen R_{a}} - k^{GnRH}_{deg} * X_{GnRH}
\end{equation}
"""

rga = r"""
\begin{equation}
    h_{R_{G,a}}(G\mhyphen R_{a}, GnRH, R_{G,a}, R_{G,i}) \\ = k^{GnRH}_{off} * X_{G\mhyphen R_{a}} - k^{GnRH}_{on} * X_{GnRH} * X_{R_{G,a}} - k^{R_{G}}_{inter} * X_{R_{G,a}} + k^{R_{G}}_{recy} * X_{R_{G,i}}
\end{equation}
"""

rgi = r"""
\begin{equation}
    h_{R_{G,i}}(G\mhyphen R_{i}, R_{G,a}, R_{G,i}) \\ = k^{G\mhyphen R_{i}}_{diss} * X_{G\mhyphen R_{i}} + k^{R_{G}}_{inter} * X_{R_{G,a}} - k^{R_{G}}_{recy} * X_{R_{G,i}} + k^{R_{G}}_{syn} - k^{R_{G}}_{degr} * X_{R_{G,i}}
\end{equation}
"""

gra = r"""
\begin{equation}
    h_{G\mhyphen R_{a}}(GnRH, R_{G,a}, G\mhyphen R_{a}, G\mhyphen R_{i}) \\ = k^{GnRH}_{on} * X_{GnRH} * X_{R_{G,a}} - k^{GnRH}_{off} * X_{G\mhyphen R_{a}} - k^{G\mhyphen R}_{inact} * X_{G\mhyphen R_{a}} + k^{G\mhyphen R}_{act} * X_{G\mhyphen R_{i}}
\end{equation}
"""

gri = r"""
\begin{equation}
    h_{G\mhyphen R_{i}}(G\mhyphen R_{a}, G\mhyphen R_{i}) \\ = k^{G\mhyphen R}_{inact} * X_{G\mhyphen R_{a}} - k^{G\mhyphen R}_{act} * X_{G\mhyphen R_{i}} - k^{G\mhyphen R}_{degr} * X_{G\mhyphen R_{i}} - k^{G\mhyphen R_{i}}_{diss} * X_{G\mhyphen R_{i}}
\end{equation}
"""

eques = [lh_pit, lh_blood, fsh_pit, fsh_blood, rfsh, fshr, rfshdes, rlh, lhr,
         rlhdes, eqs, af1, af2, af3, af4, prf, ovf, sc1, sc2, lut1, lut2, lut3,
         lut4, e2, p4, iha, ihb, ihae, gnrh, rga, rgi, gra, gri]
