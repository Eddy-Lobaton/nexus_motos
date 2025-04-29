const data = [
    {fecha: 'Nexus', proveedor: '200SS', usuario: '200', costo_total: '2020', tipo_documento: 99, nro_documento: 46, },
    {fecha: 'Nexus', proveedor: '200SS', usuario: '200', costo_total: '2020', tipo_documento: 99, nro_documento: 46, },
    {fecha: 'Nexus', proveedor: '200SS', usuario: '200', costo_total: '2020', tipo_documento: 99, nro_documento: 46, },
    {fecha: 'Nexus', proveedor: '200SS', usuario: '200', costo_total: '2020', tipo_documento: 99, nro_documento: 46, },
    {fecha: 'Nexus', proveedor: '200SS', usuario: '200', costo_total: '2020', tipo_documento: 99, nro_documento: 46, },
    {fecha: 'Nexus', proveedor: '200SS', usuario: '200', costo_total: '2020', tipo_documento: 99, nro_documento: 46, },
    {fecha: 'Nexus', proveedor: '200SS', usuario: '200', costo_total: '2020', tipo_documento: 99, nro_documento: 46, },
    {fecha: 'Nexus', proveedor: '200SS', usuario: '200', costo_total: '2020', tipo_documento: 99, nro_documento: 46, },
    {fecha: 'Nexus', proveedor: '200SS', usuario: '200', costo_total: '2020', tipo_documento: 99, nro_documento: 46, },
    {fecha: 'Nexus', proveedor: '200SS', usuario: '200', costo_total: '2020', tipo_documento: 99, nro_documento: 46, },

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