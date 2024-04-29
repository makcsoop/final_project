let username = document.getElementById('username');

function login_get(){
    let username = document.getElementById('login').value;
    return username;
};

function password_get() {
       var password = document.getElementById('pass').value;
       return password
};

if(typeof(String.prototype.trim) === "undefined")
{
    String.prototype.trim = function()
    {
        return String(this).replace(/^\s+|\s+$/g, '');
    };
}

window.onload = () => {
    document.getElementById('sign_in').onclick = () => {
        document.querySelector("#sign_in").addEventListener("click", Handler);
        let model = new Array();
        function Handler(event) {
            fetch('/app1')
                .then((response) => {
                    return response.json();
                })
                .then((myjson) => {

                    let login = login_get().trim();
                    for (var i = 1; i <= Object.keys(myjson).length; ++i){
                        if(login === myjson[i][0]) {
                            let password = password_get().trim();
                            if(password === myjson[i][1] && myjson[i][2] === 'user'){
                                $(".btn-animate").toggleClass("btn-animate-grow");
                                document.location = 'user';
                                break;
                            } else if (password === myjson[i][1] && myjson[i][2] === 'admin'){
                                var phototval = new XMLHttpRequest();
                                phototval.open('GET', "/admin?FIO=" + myjson[i][4] + '&email=' + myjson[i][4], true);
                                phototval.send();
                                document.location = 'admin/profile';
                                break;
                            }
                            else if (i === Object.keys(myjson).length) {
                                Swal.fire("Ой!", "Неверно введен логин или пароль", "error");
                                break;
                            }
                        } else if (i === Object.keys(myjson).length) {
                            Swal.fire("Ой!", "Неверно введен логин или пароль", "error");
                            break;
                        }
                    }
                });
        }
    }
}
