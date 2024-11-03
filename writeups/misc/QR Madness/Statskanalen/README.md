QR Madness CTF Challenge Writeup
================================

### Solution

First we use `zbarimg` to parse the QR codes. It parses all QRs found in single
images so the output is all the text strings found by order. We throw stderr
into `/dev/null` to omit the status line at the end of the command.

```shell
$ zbarimg ./qr.png 2> /dev/null
QR-Code:https://127.0.0.1/t
QR-Code:https://127.0.0.1/i
QR-Code:https://127.0.0.1/.
QR-Code:https://127.0.0.1/g
QR-Code:https://127.0.0.1/n
QR-Code:https://127.0.0.1/i
QR-Code:https://127.0.0.1/t
QR-Code:https://127.0.0.1/e
QR-Code:https://127.0.0.1/k
QR-Code:https://127.0.0.1/r
[...]
```

At this point we see there is a `QR-Code:https://127.0.0.1/` prefix to all of
the output. Lets use `awk` to parse out the last part of the URL with the
interesting letters.

```shell
$ zbarimg ./qr.png 2> /dev/null | awk -F\/ '{print $4}'
t
i
.
g
n
i
t
e
k
r
[...]
```

To make it easier to spot out any flags we remove the newline from the output
using `tr -d '\n'`.

```shell
$ zbarimg ./qr.png 2> /dev/null | awk -F\/ '{print $4}'| tr -d '\n'
ti.gnitekramlarenegdna,tnemeganamtnemucod,gnikcartemit,noitacifitnedimeti,gnikcarttcudorpsahcussnoitacilppaniyticapacegarots-atadretaergdnaegamilacitpoehtfo}4202_d3nw0_ts3uq_RQ{TPEgnidaerretsaffoesuacebyrtsudnielibomotuaehtdnoyebdeilppasawmetsysgnilebalRQeht,sedocrabCPUdradnatsotderapmoC.ijnak)vi(dna,yranibroetyb)iii(,ciremunahpla)ii(,ciremun)I(:gnidocnefosedomdezidradnatsruofesusedocRQ,yltneiciffeataderotsoT.gnikcart-bewdna,reifitnedina,rotacolarofatadehtsniatnocedocRQeht,metidelebalehtotcificepsnoitamrofnisniatnoctahtegamilacitpoelbadaer-enihcamasiedocrabasaerehWegamiRQehtfostnenopmoclacitrevehtdnalatnozirohehthtobnitneserperatahtsnrettapmorfdetcartxenehteraatadderiuqerehT.deterpretniyletairporppaebnacegamiehtlitnunoitcerrocrorrenomoloS–deeRgnisudessecorpdna,saremacekilsecivedgnigamiybelbadaer,srekramlaicudifhtiwdnuorgkcabetihwanoserauqskcalbserutaeftI.strapelibomotuagnillebalrofevaWosneDynapmocesenapaJyb,4991nidetnevni,edocrabxirtamlanoisnemid-owtfoepytasiedocRQA% 
```

Looking through the output we see the following string that looks like a
reversed flag `}4202_d3nw0_ts3uq_RQ{TPE`.

Lets add `rev` to reverse the output, and add a `grep -o "EPT{.*}"` to give us the flag.

```shell
$ zbarimg ./qr.png 2> /dev/null | awk -F\/ '{print $4}' | tr -d '\n' | rev | grep -Eo "EPT{.*}"
EPT{QR_qu3st_0wn3d_2024}
```
