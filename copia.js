var meta = 20000;
var venda = 25000

if (venda < meta) {
    console.log("Não atingiu a meta")
}
else if (venda > (meta*2)) {
    var bonus = 0.07*venda
    console.log(`Você ganhou um bônus de R$${bonus}`)
}
else {
    var bonus = 0.03*venda
    console.log(`Você ganhou um bônus de R$${bonus}`)
}

 