const data = [
    {fecha: 'Nexus', tipo_comprobante : '200SS', monto_efec: '150', subtotal: '2020', igv: 99, total: 46, dni_cliente: 46, vendedor: 343232, metodo_pago: 'Activo'},
    {fecha: 'Nexus', tipo_comprobante : '200SS', monto_efec: '150', subtotal: '2020', igv: 99, total: 46, dni_cliente: 46, vendedor: 343232, metodo_pago: 'Activo'},
    {fecha: 'Nexus', tipo_comprobante : '200SS', monto_efec: '150', subtotal: '2020', igv: 99, total: 46, dni_cliente: 46, vendedor: 343232, metodo_pago: 'Activo'},
    {fecha: 'Nexus', tipo_comprobante : '200SS', monto_efec: '150', subtotal: '2020', igv: 99, total: 46, dni_cliente: 46, vendedor: 343232, metodo_pago: 'Activo'},
    {fecha: 'Nexus', tipo_comprobante : '200SS', monto_efec: '150', subtotal: '2020', igv: 99, total: 46, dni_cliente: 46, vendedor: 343232, metodo_pago: 'Activo'},
    {fecha: 'Nexus', tipo_comprobante : '200SS', monto_efec: '150', subtotal: '2020', igv: 99, total: 46, dni_cliente: 46, vendedor: 343232, metodo_pago: 'Activo'},
    {fecha: 'Nexus', tipo_comprobante : '200SS', monto_efec: '150', subtotal: '2020', igv: 99, total: 46, dni_cliente: 46, vendedor: 343232, metodo_pago: 'Activo'},
    {fecha: 'Nexus', tipo_comprobante : '200SS', monto_efec: '150', subtotal: '2020', igv: 99, total: 46, dni_cliente: 46, vendedor: 343232, metodo_pago: 'Activo'},
    {fecha: 'Nexus', tipo_comprobante : '200SS', monto_efec: '150', subtotal: '2020', igv: 99, total: 46, dni_cliente: 46, vendedor: 343232, metodo_pago: 'Activo'},
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
        <td>${item.tipo_comprobante}</td>
        <td>${item.monto_efec}</td>
        <td>${item.subtotal}</td>
        <td>${item.igv}</td>
        <td>${item.total}</td>
        <td>${item.dni_cliente}</td>
        <td>${item.vendedor}</td>
        <td>${item.metodo_pago}</td>
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