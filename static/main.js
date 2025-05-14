const form = document.getElementById('form');
form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formdata = new FormData(form);
    const response = await fetch("/compile", {
        method: "post",
        body: formdata
    });

    if (response.ok && response.headers.get('Content-Disposition')) {
        const fileBlob = await response.blob();
        const link = document.createElement('a');
        link.href = URL.createObjectURL(fileBlob);
        link.download = "compiled.exe";
        link.click();
        link.style.display = 'none';
        fetch("/delete"); // No need to check response here if download was successful
    } else {
        const errorData = await response.json();
        alert("An unexpected error occurred during compilation." + errorData);
    }
});
