

    const fileInput = document.getElementById("fileInput");
    const nomesAtuais = document.getElementById("nomesAtuais");
    const novosNomes = document.getElementById("novosNomes");
    const btnDividir = document.getElementById("btnDividir");
    const resultado = document.getElementById("resultado");
    const dropZone = document.getElementById("dropZone");
    const numeroPartesInput = document.getElementById("numeroPartes");
    const camposPartes = document.getElementById("camposPartes");


    let arquivosSelecionados = [];
    let partesConfig = [];


    function extrairNomesPorPosicao() {
        let inicio = parseInt(document.getElementById("extrairInicio").value, 10);
        let fim = parseInt(document.getElementById("extrairFim").value, 10);

        const novos = arquivosSelecionados.map(file => {
            const nomeSemExtensao = file.name.replace(/\.pdf$/i, "");
            const tamanho = nomeSemExtensao.length;

            const start = isNaN(inicio) ? 0 : Math.max(0, inicio - 1);
            const end = isNaN(fim) ? tamanho : Math.min(fim, tamanho);

            return nomeSemExtensao.substring(start, end);
        });

        novosNomes.value = novos.join("\n");
    }

    document.getElementById("btnExtrairNomes").addEventListener("click", extrairNomesPorPosicao);


    function log(msg, append = true) {
        if (append) resultado.textContent += msg + "\n";
        else resultado.textContent = msg + "\n";
    }

    function habilitarBotoes(habilitar) {
        btnDividir.disabled = !habilitar;
    }

    function atualizarLista() {
        if (!arquivosSelecionados.length) {
            nomesAtuais.value = "";
            habilitarBotoes(false);
            return;
        }
        nomesAtuais.value = arquivosSelecionados.map(f => f.name).join("\n");
        habilitarBotoes(true);
        log(`✅ ${arquivosSelecionados.length} arquivo(s) selecionado(s)`, false);
    }
    function renderizarCamposPartes(qtd) {
        camposPartes.innerHTML = "";
        partesConfig = [];

        for (let i = 0; i < qtd; i++) {
            const wrapper = document.createElement("div");
            wrapper.className = "d-flex justify-content-start align-items-center w-100 p-2 split-names";

            const titulo = document.createElement("strong");
            titulo.textContent = `Parte ${i + 1}`;

            const inputPrefixo = document.createElement("input");
            inputPrefixo.type = "text";
            inputPrefixo.placeholder = "Prefixo";

            const inputSufixo = document.createElement("input");
            inputSufixo.type = "text";
            inputSufixo.placeholder = "Sufixo";

            wrapper.appendChild(titulo);
            wrapper.appendChild(inputPrefixo);
            wrapper.appendChild(inputSufixo);

            camposPartes.appendChild(wrapper);

            partesConfig.push({
                prefixo: inputPrefixo,
                sufixo: inputSufixo
            });
        }
    }
    renderizarCamposPartes(1);
    function adicionarArquivos(fileList) {
        for (let file of fileList) {
            if (!arquivosSelecionados.some(f => f.name === file.name)) {
                arquivosSelecionados.push(file);
            }
        }
        atualizarLista();
    }
    function montarNome(base, prefixo, sufixo, partePadrao) {
        let pre;
        let suf;

        if (prefixo && prefixo.trim() !== "") {
            pre = prefixo.trim();
        } else {
            pre = partePadrao;
        }

        if (sufixo && sufixo.trim() !== "") {
            suf = sufixo.trim();
        } else {
            suf = "";
        }

        return pre + base + suf + ".pdf";
    }
    function obterBaseNameParaDivisao(file) {
        const linhas = novosNomes.value.split("\n").map(l => l.trim());

        if (!linhas.length || linhas.every(l => l === "")) {
            return file.name.replace(/\.pdf$/i, "");
        }

        const index = arquivosSelecionados.findIndex(f => f.name === file.name);

        if (index !== -1 && linhas[index]) {
            return linhas[index].replace(/\.pdf$/i, "");
        }

        return file.name.replace(/\.pdf$/i, "");
    }


    function baixarArquivo(blob, nome) {
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = nome;
        link.click();
    }

    numeroPartesInput.addEventListener("change", () => {
        const qtd = parseInt(numeroPartesInput.value, 10);

            renderizarCamposPartes(qtd);
    });

    fileInput.addEventListener("change", () => {
        adicionarArquivos(fileInput.files);
    });

    dropZone.addEventListener("click", () => fileInput.click());

    dropZone.addEventListener("dragover", e => {
        e.preventDefault();
        dropZone.classList.add("dragover");
    });

    dropZone.addEventListener("dragleave", () => {
        dropZone.classList.remove("dragover");
    });

    dropZone.addEventListener("drop", e => {
        e.preventDefault();
        dropZone.classList.remove("dragover");
        adicionarArquivos(e.dataTransfer.files);
    });


    btnDividir.addEventListener("click", async () => {
        const pdfs = arquivosSelecionados.filter(f => f.type === "application/pdf");
        if (!pdfs.length) {
            alert("Selecione PDFs válidos.");
            return;
        }
        await dividirVariosPdfs(pdfs);
    });

    async function gerarZipRenomeado(files, novos) {
        const zip = new JSZip();
        log("🔄 Gerando ZIP...", false);

        files.forEach((file, i) => {
            let nome = novos[i];
            const extensao = file.name.split(".").pop();
            if (!nome.toLowerCase().endsWith("." + extensao.toLowerCase())) {
                nome += "." + extensao;
            }

            zip.file(nome, file);
            log(`${file.name} → ${nome}`);
        });

        const content = await zip.generateAsync({ type: "blob" });
        baixarArquivo(content, "arquivos_renomeados.zip");
        log("✅ ZIP gerado!");
    }

    async function dividirVariosPdfs(files) {
        const zip = new JSZip();

        for (const file of files) {
            await processarPdf(file, zip);
        }

        const content = await zip.generateAsync({ type: "blob" });
        baixarArquivo(content, "pdfs_divididos.zip");
        log("📦 PDFs divididos com sucesso!");
    }

    async function processarPdf(file, zip) {
        const buffer = await file.arrayBuffer();
        const pdfDoc = await PDFLib.PDFDocument.load(buffer);

        const totalPaginas = pdfDoc.getPageCount();
        const numeroPartes = parseInt(numeroPartesInput.value, 10);


        const paginasPorParte = Math.ceil(totalPaginas / numeroPartes);
        const baseName = obterBaseNameParaDivisao(file);

        for (let i = 0; i < numeroPartes; i++) {
            const inicio = i * paginasPorParte;
            const fim = Math.min(inicio + paginasPorParte, totalPaginas);

            if (inicio >= fim) break;

            const novoPdf = await PDFLib.PDFDocument.create();
            const paginas = [];

            for (let p = inicio; p < fim; p++) {
                paginas.push(p);
            }

            const copias = await novoPdf.copyPages(pdfDoc, paginas);
            copias.forEach(p => novoPdf.addPage(p));

            const nome = montarNome(
                baseName,
                partesConfig[i]?.prefixo?.value || "",
                partesConfig[i]?.sufixo?.value || "",
                numeroPartes > 1 ? `PARTE_${i + 1}_` : ""
            );

            zip.file(nome, await novoPdf.save());
        }
    }


