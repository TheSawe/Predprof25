let field = document.getElementById("field");
// let array = Array(256).fill(464).map(() => Array(256));

let string = "";

for (let i = 0; i < 256; i++) {
    string += "\n";
    for (let j = 0; j < 256; j++) {
        field.innerHTML = field.innerHTML += " " + 0;
    }
}