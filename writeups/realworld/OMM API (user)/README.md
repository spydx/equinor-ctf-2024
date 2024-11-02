# OMM API (user)
Author: klarz, vcpo

Flag: `EPT{Y0U_JU57_P0PP3D_7H3_4P1!}`
## Description
```
During our annual MAD pentest, we discovered a server with FastAPI running with /docs enabled.

By exploiting vulnerabilities in this API, we were able to first compromise the server hosting it and ultimately privesc to root which lead to a full Azure subscription compromise.

This challenge contains a copy of this API, glhf.

The user flag can be obtained by executing the /home/&lt;user&gt;/user binary and reading its standard output.

**NOTE: We did not transfer all the files from the original VM, so some files might be missing/mocked. The internal server errors and semi broken API is as realistic as it gets 😅**
```

