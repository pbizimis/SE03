function read_while(par) {
    console.log(par)
}
var ch = "."
function test() {
    var number = read_while(function(ch){
        console.log(ch);
        if (ch == ".") {
            return "Hello";
        }
        return "No";
    });
    console.log(number);
}

test();