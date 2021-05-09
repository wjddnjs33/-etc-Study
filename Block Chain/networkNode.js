const Blockchain = require('./Blockchain');
const express = require('express');
const bodyparser = require('body-parser');
const rp = require('request-promise');
const uuid = require('uuid');

const app = express();

app.use(bodyparser());
app.use(bodyparser.urlencoded({extended:true}));

const bitcoin = new Blockchain();

const nodeAddress = uuid.v1().split('-').join('');
const port = process.argv[2];

app.get('/', function(req, res){
    res.send(bitcoin);
});

app.get('/transaction', function(req, res){
    console.log(req.query.sender)
    const blockIndex = bitcoin.createNewBlock(req.query.amount, req.query.sender, req.query.recipient);

    res.json({note: `트랜젝션은 ${blockIndex} 블락 안으로 들어 갈 예정입니다.`});
});

app.get('/mine', function(req, res){
    const lastBlock = bitcoin.getLastBlock();
    const PreviousBlockHash = lastBlock['hash'];

    const CurrentBlockData = {
        transaction: bitcoin.pendingTransaction,
        index: lastBlock['index'] + 1
    };

    const nonce = bitcoin.proofOfWork(PreviousBlockHash, CurrentBlockData);
    const blockHash = bitcoin.hashBlock(PreviousBlockHash, CurrentBlockData, nonce)

    bitcoin.createNewTransaction(10, "Gift", nodeAddress);

    const newBlock = bitcoin.createNewBlock(nonce, PreviousBlockHash, blockHash);

    res.json({
        note: "새로운 블락이 성공적으로 생성되었습니다.",
        newBlock: newBlock
    });
});

// Don't Using
app.post('/register-and-broadcast-node', function(req, res){
    const newNodeUrl = req.body.netNodeUrl;

    if(bitcoin.networkNodes.indexOf(newNodeUrl) == -1){
        bitcoin.networkNodes.push(newNodeUrl);
    }

    const regNodePromies = [];

    bitcoin.networkNodes.forEach(networkNodesUrl => {
        const requestOption = {
            uri: networkNodesUrl + '/register-node',
            method: 'POST',
            body: {netNodeUrl:newNodeUrl},
            json:true
        };

        regNodePromies.push(rp(requestOption));
    });

    Promise.all(regNodePromies)
    .then(data => {
        const bulkRegisterOption = {
            uri: newNodeUrl + '/register-nodes-bulk',
            method: 'POST',
            body: {allNetworkNode : [...bitcoin.networkNodes, bitcoin.currentNodeUrl]},
            json: true
        };

        return rq(bulkRegisterOption);
    }).then(data => {
        res.json({note: "새로운 노드가 전체 네트워크에 성공적으로 등록이 되었습니다."});
    });
});

const pathAssignment = (obj, path, value) => {
    var segments = path.split(".");
    var key = segments.splice(0,1)[0];
    if(segments.length) {
        if(obj[key]) {
            obj[key] = pathAssignment(obj[key], segments.join('.'), value);
        } else {
            obj[key] = pathAssignment({}, segments.join('.'), value);
        }
    } else {
        obj[key] = value;
    }
    return obj;
};

app.post('/register-node', function(req, res){
    const newNodeUrl = req.body.newNodeUrl;
    const nodeNotAlreadyPresent = bitcoin.networkNodes.indexOf(newNodeUrl) == -1;
    const notCurrentNode = bitcoin.currentNodeUrl !== newNodeUrl;

    if(nodeNotAlreadyPresent&&notCurrentNode){
        bitcoin.networkNodes.push(newNodeUrl);
        result = pathAssignment({}, newNodeUrl, data);
        res.json(result)
    }

})

app.post('/register-nodes-bulk', function(req, res){
//empty
})

app.listen(port, function(){
    console.log(`Listening on Port 3000 : http://localhost:${port}`);
})