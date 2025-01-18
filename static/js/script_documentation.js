function loadDoc(filename) {
  
    // Remove o destaque de todos os links
  document.querySelectorAll(".endpointsDoc a, .sidenav a").forEach((link) => {
    link.classList.remove("active");
  });

  // Adiciona o destaque ao link clicado
  const activeLink = document.getElementById(
    `link-${filename.replace(".md", "")}`
  );

  const activeLinkMobile = document.getElementById(
    `link-${filename.replace(".md", "")}-mobile`
  );

  if (activeLink) activeLink.classList.add("active");
  if (activeLinkMobile) activeLinkMobile.classList.add("active");

  if (filename == 'inicio')
    return;

  // Faz a requisição para carregar o conteúdo do documento
  fetch("/doc/" + filename)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Document not found");
      }
      return response.text();
    })
    .then((data) => {
      document.getElementById("doc-content").innerHTML = data;
      hljs.highlightAll(); // Destaca o código, se houver
    })
    .catch((error) => {
      document.getElementById("doc-content").innerHTML =
        "<p class='center-align'>Document not found.</p>";
      console.error("Error loading document:", error);
    });
}