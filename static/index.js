window.onload=function(){

	if(error!=""){
		Swal.fire({
			icon: 'error',
			title: error,
		  })
	}

	

	if(model == "stef"){
		document.getElementById("stef").classList.add("selected")
		document.getElementById("cam").classList.add("not_selected")
	}
	else{
		document.getElementById("cam").classList.add("selected")
		document.getElementById("stef").classList.add("not_selected")	
	}


	
	(function(){
		let divLettres = document.getElementById("divLettres")

		for (let index = 65; index <= 90; index++) {
			afficheBtn(divLettres,index)
		}

	})()

};


//////////////////////// sélectionner user playlist /////////////////////////

function selectUser(el){
	
	console.log(el)
	console.log(el.parentNode)

	let previousUser = el.parentNode.querySelector(".selected")
	let nb_titres = document.getElementById("nb_titres")
	nb_titres.innerText=""
	
	previousUser.classList.remove("selected")
	previousUser.classList.add("not_selected")
	el.classList.remove("not_selected")
	el.classList.add("selected")

	deleteElement()

	let userName = el.getAttribute("alt")
	getFetch("/selectUser/"+userName,"GET", function(){
				 
		Swal.fire('La playlist de '+userName+' est sélectionné.')
	})
}


//////////////////////// chargement titre /////////////////////////

function chargerTitre(){

	Swal.fire({
		title: 'Chargement du titre...',
		showConfirmButton: false
	});
	
}

//////////////////////// charger afficher playlist /////////////////////////
	
function affichePlaylist(){

	getFetch("playlist", "GET", function(data){

		afficheTitre(data)
	})
}

//////////////////////// supprimer fichier dans playlist /////////////////////////

function deleteFile(el){

	let fichier = el.getAttribute("name")

	Swal.fire({
		title: 'Voulez vous supprimer le titre : "'+fichier+'"?',
		showDenyButton: true,
		showCancelButton: false,
		confirmButtonText: 'Oui',
		denyButtonText: `Non`,

	  }).then((result) => {
		if (result.isConfirmed) {

			getFetch("supprimer/"+fichier,"GET", function(data){

				Swal.fire('Le titre "'+fichier+'" a été supprimé.')
				affichePlaylist()
			})
		} 
		else if (result.isDenied) {
			swal.close()
		}
	  })
	
}

//////////////////////// renomme fichier dans playlist /////////////////////////

function renameFile(el){

	let ancienNom = el.getAttribute('name')

	Swal.fire({
		title: 'Nouveau nom :',
		html:
		'<input id="newName" type="text" value="'+ancienNom+'"></input',
		showCancelButton: true,
		confirmButtonText: 'ok',
		showLoaderOnConfirm: true,
		preConfirm: (nom) => {
			let name = document.getElementById("newName")
			newName = name.value

			return getFetch('/renameFile/'+newName+'/'+ancienNom, 'GET', function(data){
				Swal.fire('Le titre "'+ancienNom+'" a été renommé en "'+data.nom+'".')
			})

		}
	  })
	  
}

//////////////////////// affiche dernier fichier téléchargé dans playlist /////////////////////////

function afficheDernierDL(){
	getFetch('dernierDl','GET',function(data){
		if(data.status==200){
			console.log(data)
			afficheTitre(data)
		}
		else{
			Swal.fire(data.error)
		}
	})
}

//////////////////////// affiche fichier par la première lettre d'artiste dans playlist /////////////////////////

function lettreArtistes(el){

	let lettre = el.innerText

	getFetch("playlist/"+lettre,"GET",function(data){

		if(data.status==200){
			afficheTitre(data)
		}
		else{
			Swal.fire('il n\'y a pas d\'artistes dont le nom commence par "'+lettre+'".')
		}

	})
}
