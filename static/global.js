function afficheElement(node,data){

    let clone=node.cloneNode(true)
    let liClone=clone.querySelector("li");
    liClone.innerText=data
    let lstBtn=clone.querySelectorAll("button")

    lstBtn.forEach(btn => 
        btn.setAttribute("name", data)
    );

    clone.classList.remove("d-none")
    clone.classList.add("show")
    node.parentNode.append(clone)
}




function afficheBtn(node,index){
    let btn = node.querySelector("button")
    let clone = btn.cloneNode(true)
    clone.innerText = String.fromCharCode(index)
    node.appendChild(clone)
}




function getFetch(url, method, fonction){

    fetch("http://127.0.0.1:5000/"+url, {method: method})	
    .then(function(response) {
        return response.json()
    })
    .then(function(data){

        if(data.error){
            Swal.fire({
                icon: 'error',
                title: data.error
              })
        }
    
        fonction(data)
    })
    .catch(function(error) {
        console.log('Il y a eu un problème avec l\'opération fetch: ' + error.message);
    })
    
}




function deleteElement(el=null){

    if(el==null){
        el = document.getElementById("li_playlist")
    }

    if(el.parentNode.getElementsByClassName("show").length>0){
        let lstShow=Array.from(el.parentNode.getElementsByClassName("show"))
        lstShow.forEach(el => el.remove())
    }
}




function afficheTitre(data){

    let liListe = document.getElementById("li_playlist")
    let nb_titres = document.getElementById("nb_titres")

    deleteElement(liListe)
        
    nb_titres.innerText=data.titres.length

    data.titres.forEach(titre => 
            afficheElement(liListe,titre)
    );
}
