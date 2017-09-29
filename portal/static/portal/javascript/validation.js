function check_req(){
    var x,text;
     x = document.forms["login"]["id_username"].value;

    if (x == ""){
       text = "field required";
    }
    else{
        text = "input is ok";
    }
     document.getElementById("print").innerHTML = text;
}





