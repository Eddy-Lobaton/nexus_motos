const data = [
    {nombre: 'MOTOS CAR EIRL', ruc: '234345465652', telefono: '949 393 993', direccion: 'Madre de Dios', email: 'motoscar@gmail.com', editar: 46, },
    {nombre: 'NITRO MOTOS SAC', ruc: '2442334d2342', telefono: '934 343 267', direccion: 'Huancayo ', email: 'nitromotos@gmail.com', editar: 46, },
    {nombre: 'NITRO MOTOS SAC', ruc: '243345465652', telefono: '934 346 234', direccion: 'Huancayo', email: 'nitromotos@gmail.com', editar: 46, },
    {nombre: 'NITRO MOTOS SAC', ruc: '23435465652', telefono: '934 234 123', direccion: 'Huancayo', email: 'nitromotos@gmail.com', editar: 46, },
    {nombre: 'MOTOS CAR EIRL', ruc: '234345465652', telefono: '934 453 123', direccion: 'Cusco', email: 'motoscar@gmail.com', editar: 46, },
    {nombre: 'NITRO MOTOS SAC', ruc: '234345465652', telefono: '934 343 555', direccion: 'Cusco', email: 'nitromotos@gmail.com', editar: 46, },
    {nombre: 'MOTOS CAR EIRL', ruc: '234345465652', telefono: '934 342 332', direccion: 'Huancayo', email: 'motoscar@gmail.com', editar: 46, },
    {nombre: 'CARMOTOR SAC', ruc: '234345465652', telefono: '933 343 123', direccion: 'Huancayo', email: 'carmotor@gmail.com', editar: 46, },
    {nombre: 'CARMOTOR SAC', ruc: '234345465652', telefono: '934 341 234', direccion: 'Huancayo', email: 'carmotor@gmail.com', editar: 46, },
    {nombre: 'MOTOS CAR EIRL', ruc: '234345465652', telefono: '923 346 342', direccion: 'Huancayo', email: 'motoscar@gmail.com', editar: 46, },

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