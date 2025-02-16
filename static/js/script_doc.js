
function loadDoc(filename) {

  // Remove o destaque de todos os links
  document.querySelectorAll(".endpointsDoc a").forEach((link) => {
    link.classList.remove("active");
  });

  // Adiciona o destaque ao link clicado
  const activeLink = document.getElementById(
    `link-${filename.replace(".md", "")}`
  );

  if (activeLink) activeLink.classList.add("active");

  if (filename == 'inicio') return;

  // Faz a requisição para carregar o conteúdo do documento
  fetch("/doc/" + filename)

    .then((response) => {
      if (!response.ok) {
        throw new Error("Document not found");
      }
      return response.text();
    })
    
    .then((data) => {

      // Renderiza o Markdown e escapa o HTML
      const renderedContent = marked.parse(data);
      document.getElementById("doc-content").innerHTML = renderedContent;
      
      // Aplica o highlight.js ao código gerado
      hljs.highlightAll();
    })

    .catch((error) => {
      document.getElementById("doc-content").innerHTML =
        "<p class='center-align'>Document not found.</p>";
      console.error("Error loading document:", error);
    });
}