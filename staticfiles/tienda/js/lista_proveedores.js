const data = [
    {nombre: 'Nexus', ruc: '200SS', telefono: '200', direccion: '2020', email: 99, editar: 46, },
    {nombre: 'Nexus', ruc: '200SS', telefono: '200', direccion: '2020', email: 99, editar: 46, },
    {nombre: 'Nexus', ruc: '200SS', telefono: '200', direccion: '2020', email: 99, editar: 46, },
    {nombre: 'Nexus', ruc: '200SS', telefono: '200', direccion: '2020', email: 99, editar: 46, },
    {nombre: 'Nexus', ruc: '200SS', telefono: '200', direccion: '2020', email: 99, editar: 46, },
    {nombre: 'Nexus', ruc: '200SS', telefono: '200', direccion: '2020', email: 99, editar: 46, },
    {nombre: 'Nexus', ruc: '200SS', telefono: '200', direccion: '2020', email: 99, editar: 46, },
    {nombre: 'Nexus', ruc: '200SS', telefono: '200', direccion: '2020', email: 99, editar: 46, },
    {nombre: 'Nexus', ruc: '200SS', telefono: '200', direccion: '2020', email: 99, editar: 46, },
    {nombre: 'Nexus', ruc: '200SS', telefono: '200', direccion: '2020', email: 99, editar: 46, },

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
        <td>${item.nombre}</td>
        <td>${item.ruc}</td>
        <td>${item.telefono}</td>
        <td>${item.direccion}</td>
        <td>${item.email}</td>
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