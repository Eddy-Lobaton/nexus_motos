document.addEventListener("DOMContentLoaded", function() {
    const codigoInput = document.getElementById('codigo');
    const barcode = document.getElementById('barcode');
    const printBtn = document.getElementById('print-barcode');
    const downloadBtn = document.getElementById('download-barcode');

    codigoInput.addEventListener('input', function() {
        const value = codigoInput.value.trim();
        if (value) {
            JsBarcode("#barcode", value, {
                format: "CODE128",
                lineColor: "#000",
                width: 2,
                height: 60,
                displayValue: true
            });
        } else {
            barcode.innerHTML = '';
        }
    });

    printBtn.addEventListener('click', function() {
        const win = window.open('', 'Imprimir Código', 'height=400,width=600');
        win.document.write('<html><head><title>Código de Barras</title></head><body>');
        win.document.write(barcode.outerHTML);
        win.document.write('</body></html>');
        win.document.close();
        win.focus();
        win.print();
        win.close();
    });

    downloadBtn.addEventListener('click', function() {
        const svgData = new XMLSerializer().serializeToString(barcode);
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();

        const svgBlob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
        const url = URL.createObjectURL(svgBlob);

        img.onload = function() {
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);
            URL.revokeObjectURL(url);

            const pngImg = canvas.toDataURL('image/png');
            const a = document.createElement('a');
            a.href = pngImg;
            a.setAttribute('download', ''); // ← Esto pide elegir ubicación
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        };
        img.src = url;
    });
});
