function habilitar(){
    if(document.getElementById('sms1').checked){
      document.getElementById('telefone').disabled = false;
    } else {
      document.getElementById('telefone').disabled = true;
    }
  }