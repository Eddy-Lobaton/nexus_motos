const data = [
    {fecha: '12/01/2024', proveedor: 'MOTOS CAR EIRL', usuario: 'eddy-lobaton', costo_total: 'S/5,000.00', tipo_documento: 'Boleta', nro_documento: 123-3454, },
    {fecha: '10/04/2024', proveedor: 'NITRO MOTOS SAC', usuario: 'jose-mamani', costo_total: 'S/6,000.00', tipo_documento: 'Boleta', nro_documento: 124-3454, },
    {fecha: '15/01/2025', proveedor: 'LIMA MOTOS EIRL', usuario: 'carlos-jose', costo_total: 'S/9,500.00', tipo_documento: 'Factura', nro_documento: 125-3454, },
    {fecha: '01/01/2025', proveedor: 'CARMOTOR SAC', usuario: 'eddy-lobaton', costo_total: 'S/4,400.00', tipo_documento: 'Factura', nro_documento: 126-3454, },
    {fecha: '10/10/2024', proveedor: 'MOTOS CAR EIRL', usuario: 'eddy-lobaton', costo_total: 'S/7,500.00', tipo_documento: 'Factura', nro_documento: 127-3454, },
    {fecha: '23/02/2025', proveedor: 'MOTOS CAR EIRL', usuario: 'jose-mamani', costo_total: 'S/5,000.00', tipo_documento: 'Boleta', nro_documento: 128-3454, },
    {fecha: '12/10/2024', proveedor: 'CARMOTOR SAC', usuario: 'carlos-jose', costo_total: 'S/6,800.00', tipo_documento: 'Boleta', nro_documento: 129-3454, },
    {fecha: '12/11/2024', proveedor: 'MOTOS CAR EIRL', usuario: 'carlos-jose', costo_total: 'S/9,400.00', tipo_documento: 'Boleta', nro_documento: 129-3454, },
    {fecha: '12/01/2025', proveedor: 'MOTOS CAR EIRL', usuario: 'jose-mamani', costo_total: 'S/3,500.00', tipo_documento: 'Boleta', nro_documento: 133-3454, },
    {fecha: '03/05/2024', proveedor: 'CARMOTOR SAC', usuario: 'jose-mamani', costo_total: 'S/5,199.00', tipo_documento: 'Boleta', nro_documento: 133-3454, },

];

const rowsPerPage = 6;
let currentPage = 1;

function renderTable() {
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = '';

    const start = (currentPage - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    const pageData = data.slice(start, end);

    for (let item of pageData) {
    tbody.innerHTML += `
        <tr>
        <td>${item.fecha}</td>
        <td>${item.proveedor}</td>
        <td>${item.usuario}</td>
        <td>${item.costo_total}</td>
        <td>${item.tipo_documento}</td>
        <td>${item.nro_documento}</td>
        <td><span class="edit-icon">✏️</span></td>
        </tr>
    `;
    }
}

function renderPagination() {
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = '';

    const pageCount = Math.ceil(data.length / rowsPerPage);

    for (let i = 1; i <= pageCount; i++) {
    const button = document.createElement('button');
    button.textContent = i;
    if (i === currentPage) {
        button.classList.add('active');
    }
    button.addEventListener('click', () => {
        currentPage = i;
        renderTable();
        renderPagination();
    });
    pagination.appendChild(button);
    }
}

renderTable();
renderPagination();