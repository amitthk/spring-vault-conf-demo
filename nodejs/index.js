const http = require('http');

const hostname = '127.0.0.1';
const port = 3000;





const server = http.createServer();

server.on('request', async (req, res) => {

    const vaultAddr = process.env.VAULT_ADDR;
    const vaultToken = process.env.VAULT_TOKEN;
    const vaultKeysPath = process.env.VAULT_KEYS_PATH;


    const vault = require("node-vault")({
      apiVersion: "v1",
      endpoint: vaultAddr,
    });

    vault.token = vaultToken
    const { data } = await vault.read(vaultKeysPath);
    let respStr = '<html><head></head><body><ul>'
    for(var key in data['data']){
    respStr = respStr + '<li>' + key + ': ' + data['data'][key] + '</li>';
    }
    respStr+= '</ul></body></html>';
    res.end(respStr);
});


server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
