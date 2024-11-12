import React, { useState } from "react";
import Pagination from "react-paginate";

function TablePagination() {
  const [currentPage, setCurrentPage] = useState(0);

  localStorage["currentPage"] = JSON.stringify({ page: "/test_pag" });

  const handlePageClick = (data) => {
    setCurrentPage(data.selected);
  };

  const itemsPerPage = 10;
  const rows = [
    { id: 1, name: "John Doe", age: 25 },
    { id: 2, name: "Jane Doe", age: 30 },
    { id: 3, name: "Jane Doe", age: 30 },
    { id: 4, name: "Jane Doe", age: 30 },
    { id: 5, name: "Jane Doe", age: 30 },
    { id: 6, name: "Jane Doe", age: 30 },
    { id: 7, name: "Jane Doe", age: 30 },
    { id: 8, name: "Jane Doe", age: 30 },
    { id: 9, name: "Jane Doe", age: 30 },
    { id: 9, name: "Jane Doe", age: 30 },
    { id: 9, name: "Jane Doe", age: 30 },
    { id: 9, name: "Jane Doe", age: 30 },
    { id: 9, name: "Jane Doe", age: 30 },
    { id: 9, name: "Jane Doe", age: 30 },
    { id: 9, name: "Jane Doe", age: 30 },
    // ...and so on
  ];
  const rowsToDisplay = rows.slice(
    currentPage * itemsPerPage,
    (currentPage + 1) * itemsPerPage,
  );

  return (
    <div>
      <h1>Table with Pagination</h1>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Age</th>
          </tr>
        </thead>
        <tbody>
          {rowsToDisplay.map((row) => (
            <tr key={row.id}>
              <td>{row.id}</td>
              <td>{row.name}</td>
              <td>{row.age}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <Pagination
        pageCount={Math.ceil(rows.length / itemsPerPage)}
        onPageChange={handlePageClick}
        containerClassName={"pagination"}
        activeClassName={"active"}
      />
    </div>
  );
}

export default TablePagination;
