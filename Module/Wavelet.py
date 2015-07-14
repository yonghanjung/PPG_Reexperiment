from numpy.ma import log2, sqrt, log
from compiler.ast import flatten
import numpy as np

def zeros(num):
    return [0] * num

def sign(mylist):
    return [abs(x) for x in mylist]


__author__ = 'jeong-yonghan'


def qmf(typename, par):
    if typename == 'haar' and par == 0:
        return [float(1 / sqrt(2)), float(1 / sqrt(2))]
    elif typename == "beylkin" and par == 0:
        return [0.0993057653740000, 0.424215360813000, 0.699825214057000,
                0.449718251149000, - 0.110927598348000, - 0.264497231446000, 0.0269003088040000,
                0.155538731877000, - 0.0175207462670000, - 0.0885436306230000, 0.0196798660440000,
                0.0429163872740000, - 0.0174604086960000, - 0.0143658079690000, 0.0100404118450000,
                0.00148423478200000, - 0.00273603162600000, 0.000640485329000000]
    elif typename == 'db':
        if par == 4:
            return [0.482962913145000, 0.836516303738000, 0.224143868042000, -0.129409522551000]
        elif par == 6:
            return [0.332670552950000, 0.806891509311000, 0.459877502118000, -0.135011020010000, -0.0854412738820000,
                    0.0352262918820000]
        elif par == 8:
            return [0.230377813309000, 0.714846570553000, 0.630880767930000, -0.0279837694170000, -0.187034811719000,
                    0.0308413818360000, 0.0328830116670000, -0.0105974017850000]
        elif par == 10:
            return [.160102397974, .603829269797, .724308528438,
                    .138428145901, -.242294887066, -.032244869585,
                    .077571493840, -.006241490213, -.012580751999,
                    .003335725285, ]
        elif par == 12:
            return [.111540743350, .494623890398, .751133908021,
                    .315250351709, -.226264693965, -.129766867567,
                    .097501605587, .027522865530, -.031582039317,
                    .000553842201, .004777257511, -.001077301085]
        elif par == 14:
            return [.077852054085, .396539319482, .729132090846,
                    .469782287405, -.143906003929, -.224036184994,
                    .071309219267, .080612609151, -.038029936935,
                    -.016574541631, .012550998556, .000429577973,
                    -.001801640704, .000353713800, ]
        elif par == 16:
            return [.054415842243, .312871590914, .675630736297,
                    .585354683654, -.015829105256, -.284015542962,
                    .000472484574, .128747426620, -.017369301002,
                    -.044088253931, .013981027917, .008746094047,
                    -.004870352993, -.000391740373, .000675449406,
                    -.000117476784, ]
        elif par == 18:
            return [.038077947364, .243834674613, .604823123690,
                    .657288078051, .133197385825, -.293273783279,
                    -.096840783223, .148540749338, .030725681479,
                    -.067632829061, .000250947115, .022361662124,
                    -.004723204758, -.004281503682, .001847646883,
                    .000230385764, -.000251963189, .000039347320]
        elif par == 20:
            return [.026670057901, .188176800078, .527201188932,
                    .688459039454, .281172343661, -.249846424327,
                    -.195946274377, .127369340336, .093057364604,
                    -.071394147166, -.029457536822, .033212674059,
                    .003606553567, -.010733175483, .001395351747,
                    .001992405295, -.000685856695, -.000116466855,
                    .000093588670, -.000013264203, ]

    elif typename == "coif":
        if par == 1:
            return [.038580777748, -.126969125396, -.077161555496,
                    .607491641386, .745687558934, .226584265197]
        elif par == 2:
            return [.016387336463, -.041464936782, -.067372554722,
                    .386110066823, .812723635450, .417005184424,
                    -.076488599078, -.059434418646, .023680171947,
                    .005611434819, -.001823208871, -.000720549445]
        elif par == 3:
            return [-.003793512864, .007782596426, .023452696142,
                    -.065771911281, -.061123390003, .405176902410,
                    .793777222626, .428483476378, -.071799821619,
                    -.082301927106, .034555027573, .015880544864,
                    -.009007976137, -.002574517688, .001117518771,
                    .000466216960, -.000070983303, -.000034599773]
        elif par == 4:
            return [.000892313668, -.001629492013, -.007346166328,
                    .016068943964, .026682300156, -.081266699680,
                    -.056077313316, .415308407030, .782238930920,
                    .434386056491, -.066627474263, -.096220442034,
                    .039334427123, .025082261845, -.015211731527,
                    -.005658286686, .003751436157, .001266561929,
                    -.000589020757, -.000259974552, .000062339034,
                    .000031229876, -.000003259680, -.000001784985]
        elif par == 5:
            return [-.000212080863, .000358589677, .002178236305,
                    -.004159358782, -.010131117538, .023408156762,
                    .028168029062, -.091920010549, -.052043163216,
                    .421566206729, .774289603740, .437991626228,
                    -.062035963906, -.105574208706, .041289208741,
                    .032683574283, -.019761779012, -.009164231153,
                    .006764185419, .002433373209, -.001662863769,
                    - .000638131296, .000302259520, .000140541149,
                    - .000041340484, -.000021315014, .000003734597,
                    .000002063806, -.000000167408, -.000000095158]
    elif typename == 'symmlet':
        if par == 4:
            return [-.107148901418, -.041910965125, .703739068656,
                    1.136658243408, .421234534204, -.140317624179,
                    -.017824701442, .045570345896, ]
        elif par == 5:
            return [.038654795955, .041746864422, -.055344186117,
                    .281990696854, 1.023052966894, .896581648380,
                    .023478923136, -.247951362613, -.029842499869,
                    .027632152958, ]
        elif par == 6:
            return [.021784700327, .004936612372, -.166863215412,
                    -.068323121587, .694457972958, 1.113892783926,
                    .477904371333, -.102724969862, -.029783751299,
                    .063250562660, .002499922093, -.011031867509]
        elif par == 7:
            return [.003792658534, -.001481225915, -.017870431651,
                    .043155452582, .096014767936, -.070078291222,
                    .024665659489, .758162601964, 1.085782709814,
                    .408183939725, -.198056706807, -.152463871896,
                    .005671342686, .014521394762, ]

        elif par == 8:
            return [0.00267279339300000, - 0.000428394300000000, - 0.0211456865280000, 0.00538638875400000,
                    0.0694904659110000, - 0.0384935212630000, - 0.0734625087610000, 0.515398670374000, 1.09910663053700,
                    0.680745347190000, - 0.0866536154060000, - 0.202648655286000, 0.0107586117510000,
                    0.0448236230420000, - 0.000766690896000000, - 0.00478345851200000]
        elif par == 9:
            return [.001512487309, -.000669141509, -.014515578553,
                    .012528896242, .087791251554, -.025786445930,
                    -.270893783503, .049882830959, .873048407349,
                    1.015259790832, .337658923602, -.077172161097,
                    .000825140929, .042744433602, -.016303351226,
                    -.018769396836, .000876502539, .001981193736]
        elif par == 10:
            return [.001089170447, .000135245020, -.012220642630,
                    -.002072363923, .064950924579, .016418869426,
                    -.225558972234, -.100240215031, .667071338154,
                    1.088251530500, .542813011213, -.050256540092,
                    -.045240772218, .070703567550, .008152816799,
                    -.028786231926, -.001137535314, .006495728375,
                    .000080661204, -.000649589896, ]


def myfilter(b, a, x):
    # MATLAB
    # a(1)*y(n) = b(1)*x(n) + b(2)*x(n-1) + ... + b(nb+1)*x(n-nb) - a(2)*y(n-1) - ... - a(na+1)*y(n-na)
    # PYTHON
    # SUM :  a[0] * y[k] = b[0]*x[k] + b[1] * x[k-1] + ... + b[len(b)-1] * x[k - len(b) -1] for k = 0 to len(x)
    # SUB : a[1] * y[k-1] + ... + a[len(a)-1]*y[k-len(a)-1]
    y = []
    x = flatten(x)
    for k in range(len(x)):
        mysum = 0
        mysub = 0
        for bi in range(len(b)):
            if k - bi >= 0:
                mysum += b[bi] * x[k - bi]
        for ai in range(1, len(a)):
            if k - ai >= 0:
                mysub += a[ai] * y[k - ai]
        y.append(float((mysum - mysub)) / float(a[0]))
    return y


def dyadlength(x):
    # x : signal
    if log2(len(x)) - int(log2(len(x))) == 0:
        return [len(x), int(log2(len(x)))]


def mirror_filt(x):
    returnvar = []
    temp = [it + 1 for it in range(len(x))]
    temp = [(-1) ** it for it in temp]
    temp = [-1 * it for it in temp]
    for i in range(len(x)):
        returnvar.append(temp[i] * x[i])
    return returnvar


def lshift(x):
    y = [x[1:len(x)], x[0]]
    y = y[0]
    y = np.array(y).tolist()
    y = flatten(y)
    return y


def iconv(f, x):
    n = len(x)
    p = len(f)
    a = [1]
    if p <= n:
        xpadded = [x[n - p: n], x]
        xpadded = [item for sublist in xpadded for item in sublist]
    else:
        z = zeros(p)
        for i in range(p):
            imod = 1 + ((p * n - p + i - 1) % n)
            z[i] = x[imod]
        xpadded = [z, x]
        xpadded = [item for sublist in xpadded for item in sublist]
    ypadded = myfilter(f, a, xpadded)
    return ypadded[p: n + p]


def aconv(f, x):
    n = len(x)
    p = len(f)
    if p < n:
        xpadded = [x, x[:p]]
        xpadded = [item for sublist in xpadded for item in sublist]
    else:
        z = zeros(p)
        for i in range(p):
            imod = 1 + (i % n)
            z[i] = x[imod]
        xpadded = [x, z]
        xpadded = [item for sublist in xpadded for item in sublist]
    fflip = [it for it in reversed(f)]
    ypadded = myfilter(fflip, [1], xpadded)
    return ypadded[p - 1:n + p - 1]


def DownDyadHi(x, qmf):
    d = iconv(mirror_filt(qmf), lshift(x))
    n = len(d)
    endval = d[len(d) - 1]
    d = d[::2]
    # if d[len(d) - 1] == endval:
    # d.remove(endval)
    return d


def DownDyadLo(x, qmf):
    d = aconv(qmf, x)
    endval = d[len(d) - 1]
    d = d[::2]
    #if d[len(d) - 1] == endval:
    #    d.remove(endval)
    return d


def dyad(j):
    startval = (2 ** j) + 1
    endval = 2 ** (j + 1)
    return [it for it in range(startval, endval + 1)]


def FWT_PO(x, L, qmf):
    n = len(x)
    J = int(log2(n))
    wcoef = zeros(n)
    for j in reversed(range(L, J)):
        alfa = DownDyadHi(x, qmf)
        for idx, i in enumerate(dyad(j)):
            wcoef[i - 1] = alfa[idx]
        x = DownDyadLo(x, qmf)
    wcoef[:2 ** L] = x
    return wcoef


def rshift(x):
    n = len(x)
    returnval = [x[n - 1], x[:n - 1]]
    return flatten(returnval)


def UpSampleN(x):
    n = len(x) * 2
    y = zeros(n)
    for idx, i in enumerate(xrange(0, n - 1, 2)):
        y[i] = x[idx]
    return y


def UpDyadHi(x, qmf):
    return aconv(mirror_filt(qmf), rshift(UpSampleN(x)))


def UpDyadLo(x, qmf):
    return iconv(qmf, UpSampleN(x))


def IWT_PO(wc, L, qmf):
    x = wc[:2 ** L]
    n = len(wc)
    J = int(log2(n))
    for j in range(L, J):
        A = UpDyadLo(x, qmf)
        B = wc[(2 ** j): 2 ** (j + 1)]
        B = UpDyadHi(B, qmf)
        x = [sum(it) for it in zip(A, B)]
    return x


def SoftThresh(y, t):
    absy = [abs(it) for it in y]
    res = [it - t for it in absy]
    absres = [abs(it) for it in res]
    res = [float(sum(it)) / float(2) for it in zip(res, absres)]
    return [a * b for a, b in zip(sign(y), res)]


def VisuThresh(y):
    thr = sqrt(2 * log(len(y)))
    return SoftThresh(y, thr)


def MultiVisu(wc, L):
    n = len(wc)
    J = int(log2(n))
    ws = wc
    wc[(2 ** L):n] = VisuThresh(wc[2 ** L: n])
    return wc


def WaveShrink(y, typename, L, qmf):
    n = len(y)
    J = int(log2(n))
    wc = FWT_PO(y, L, qmf)
    if typename == 'visu':
        wc[(2 ** L): n] = VisuThresh(wc[2 ** L: n])
    elif typename == 'sure':
        wc = MultiVisu(wc, L)
    return IWT_PO(wc, L, qmf), wc


def cutscale(wc, L):
    temp = wc
    for i in range(2 ** L):
        temp[i] = 0
    return temp


def cutwavelet(wc, L):
    temp = wc
    for i in range((2 ** L) + 1, len(wc)):
        temp[i] = 0
    return temp