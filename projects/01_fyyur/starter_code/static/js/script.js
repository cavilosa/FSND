window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

const deleteVenue = document.querySelector("#delete-venue");
if (deleteVenue != null) {
    deleteVenue.addEventListener("click", (e) => {
        e.preventDefault();
        console.log("deleteVenue", e)
        const deleteId = e.target.dataset["id"];
        fetch ("/venues/" + deleteId, {
            method:"DELETE"
        })
        .then( (response) => {  
            window.location = "/";
        })
    })
}

const deleteArtist = document.querySelector("#delete-artist");
if (deleteArtist != null) {
    deleteArtist.addEventListener("click", (e) => {
        e.preventDefault();
        console.log("deleteArtist", e)
        const deleteId = e.target.dataset["id"];
        fetch ("/artist/" + deleteId, {
            method:"DELETE"
        })
        .then( (response) => {  
            window.location = "/artists";
        })
    })
}
