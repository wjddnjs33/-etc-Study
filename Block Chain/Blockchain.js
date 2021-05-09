/*

Q : How to create a blockchain?
A : It's a job of combining multiple transaction records to form one block.

Q : What is transcation(Tx)?
A : Tx is the smallest unit of business processing that can no longer be divide.

If occur transaction in internet or online etc, each transaction composes one transaction details. 
This transaction details is encrypted using hash function.

Q : Why encrypt with a hash value?
A : All transaction details length is not same. However, the length is same in case of encryption
using the hash function.

Example)
[Transaction detail 1] "A gives B a dollar"  -> [hash_1] 4D076DE7A24858575FF93DC1E5D68BCD8A080885E9B9E7475A7B842AAFA702E0
[Transaction detail 2] "A gets $2 from B"    -> [hash_2] D29A4270D548BDC138D921DD782E5420A4E7651830CA7ACA0F11D518AC445B70
-> hash_1.length : hash_2.length = 1 : 1
*/

// Block Data Structure
const sha256 = require('sha256');

const currentNodeUrl = process.argv[3];



function Blockchain(){
    this.chain = [];
    this.pendingTransaction = [];

    this.currentNodeUrl =currentNodeUrl;
    this.networkNodes = [];
    this.createNewBlock(100, '0', '0');
}

// Define the Blockchain prototype function.
Blockchain.prototype.createNewBlock = function(nonce, previousBlockHash, hash){
    const newBlock = {
        index: this.chain.length + 1,
        timestamp: Date.now(),
        transactions: this.pendingTransaction,
        nonce: nonce,
        hash: hash,
        previousBlockHash: previousBlockHash
    };

    /* We empty the transaction details for the next transcation and add a new block 
    to the chain array.*/
    this.pendingTransaction = [];
    this.chain.push(newBlock);

    return newBlock;
}

Blockchain.prototype.getLastBlock = function(){
    return this.chain[this.chain.length - 1];
}

Blockchain.prototype.createNewTransaction = function(amount, sender, recipient){
    const newTransaction = {
        amount: amount,
        sender: sender,
        recipient: recipient
    };

    this.pendingTransaction.push(newTransaction);
    
    return this.getLastBlock()['index'] + 1;
}

Blockchain.prototype.hashBlock = function(PBH, CBD, nonce){
    return sha256(PBH + nonce.toString() + JSON.stringify(CBD));
}

Blockchain.prototype.proofOfWork = function(PBH, CBD,){
    let nonce = 0;
    let hash = this.hashBlock(PBH, CBD, nonce);

    while(hash.substring(0,4) != '0000'){
        nonce++;
        hash = this.hashBlock(PBH, CBD, nonce);
    }

    return nonce
}

module.exports = Blockchain;