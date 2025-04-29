const data = [
    {marca: 'Nexus', modelo: '200SS', motor: '150', anio: '2020', stock: 999, imagen: 46, descripcion: 46, codigo: 343232, estado: 'Calle '},
    {marca: 'Nexus', modelo: '200SS', motor: 'Nexus', anio: '2020', stock: 32, imagen: 34, descripcion: 34, codigo: 343232, estado: 'Calle'},
    {marca: 'Nexus', modelo: '200SS', motor: 'Nexus', anio: '2020', stock: 15, imagen: 27, descripcion: 27, codigo: 343232, estado: 'Activo'},
    {marca: 'Nexus', modelo: '200SS', motor: 'Nexus', anio: '2020', stock: 10, imagen: 15, descripcion: 15, codigo: 343232, estado: 'Activo'},
    {marca: 'Nexus', modelo: '200SS', motor: 'Nexus', anio: '2020', stock: 7, imagen: 14, descripcion: 14, codigo: 343232, estado: 'Activo'},
    {marca: 'Nexus', modelo: '200SS', motor: 'Nexus', anio: '2020', stock: 7, imagen: 14, descripcion: 14, codigo: 343232, estado: 'Activo'},
    {marca: 'Nexus', modelo: '200SS', motor: 'Nexus', anio: '2020', stock: 7, imagen: 14, descripcion: 14, codigo: 343232, estado: 'Activo'},
    {marca: 'Nexus', modelo: '200SS', motor: 'Nexus', anio: '2020', stock: 12, imagen: 25, descripcion: 25, codigo: 343232, estado: 'Activo'},
    {marca: 'Nexus', modelo: '200SS', motor: 'Nexus', anio: '2020', stock: 18, imagen: 20, descripcion: 20, codigo: 343232, estado: 'Activo'},
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
        <td>${item.marca}</td>
        <td>${item.modelo}</td>
        <td>${item.motor}</td>
        <td>${item.anio}</td>
        <td>${item.stock}</td>
        <td>${item.imagen}</td>
        <td>${item.descripcion}</td>
        <td>${item.codigo}</td>
        <td>${item.estado}</td>
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