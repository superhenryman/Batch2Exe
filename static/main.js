const form = document.getElementById('form');
form.addEventListener("submit", async (event) => {
    event.preventDefault();
            
    const formdata = new FormData(form);
    const response = await fetch("/compile", {
        method:"post",
        body: formdata
    });
    const fileBlob = await response.blob();
    const link = document.createElement('a');
    link.href = URL.createObjectURL(fileBlob);
    link.download = "compiled.exe";
    link.click(); 
    link.style.display = 'none';
    if (response.ok) {
        fetch("/delete")
    } else {
        alert("Error while deleting file on server")
    }
});