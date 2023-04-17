import './Pagination.css';

const Pagination = ({pageCount: pagesRange, currentPage, onPageChange, lastPage, prevPage, nextPage=2,}) => {
    // const pages = Array.from({length: pagesRange}, (_, i) => i + 1);

    const style = {
        color: "white",
        fontSize: "10px",
        border: "1px solid white",
        outlineColor: "none"
    };

    return(
        <nav>
            <ul className="pagination">
                <li className="page-item">
                    <button className="page-link bg-dark bg-opacity-50 page-button"
                            style={style}
                            onClick={() => onPageChange(1)}>
                        <b>1</b>
                    </button>
                </li>
                <li className="page-item">
                    <button className={`page-link bg-dark bg-opacity-50 page-button ${prevPage ? '' : 'disabled'}`}
                            style={style}
                            onClick={() => onPageChange(prevPage)}>
                        <b>{"<"}</b>
                    </button>
                </li>
                {pagesRange.map(page => (
                    <li key={page} className={`page-item ${page === currentPage ? 'active' : ''}`}>
                        <button className={`${page === currentPage ? 'bg-opacity-75' : 'bg-opacity-50'} page-link bg-dark page-button`}
                                style={style}
                                onClick={() => onPageChange(page)}>
                            {page}
                        </button>
                    </li>
                ))}
                <li className="page-item">
                    <button className={`page-link bg-dark bg-opacity-50 page-button ${nextPage ? '' : 'disabled'}`}
                            style={style}
                            onClick={() => onPageChange(nextPage)}>
                        <b>{">"}</b>
                    </button>
                </li>
                <li className="page-item">
                    <button className="page-link bg-dark bg-opacity-50 page-button"
                            style={style}
                            onClick={() => onPageChange(lastPage)}>
                        <b>{lastPage}</b>
                    </button>
                </li>
            </ul>
        </nav>
    );
};

export default Pagination;