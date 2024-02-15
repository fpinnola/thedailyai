import { useState } from 'react';

const PagedTextViewer = ({ text, charsPerPage = 500 }: { text: string, charsPerPage?: number }) => {
  const [currentPage, setCurrentPage] = useState(0);

  // Function to split the text into pages
  const getTextPages = (text: string) => {
    let pages = [];
    let startIndex = 0;

    while (startIndex < text.length) {
      let endIndex = Math.min(startIndex + charsPerPage, text.length);
      if (endIndex < text.length) {
        let lastSpaceIndex = text.lastIndexOf(' ', endIndex);
        let lastNewlineIndex = text.lastIndexOf('\n', endIndex);
        let cutIndex = Math.max(lastSpaceIndex, lastNewlineIndex);
        if (cutIndex <= startIndex) {
          cutIndex = endIndex;
        }
        pages.push(text.substring(startIndex, cutIndex + 1));
        startIndex = cutIndex + 1;
      } else {
        pages.push(text.substring(startIndex, endIndex));
        break;
      }
    }

    return pages;
  };

  const pages = getTextPages(text);

  // Navigation functions
  const nextPage = () => setCurrentPage((prevPage) => Math.min(prevPage + 1, pages.length - 1));
  const prevPage = () => setCurrentPage((prevPage) => Math.max(prevPage - 1, 0));

  return (
    <div>
      <div style={{ whiteSpace: 'pre-wrap' }}>{pages[currentPage]}</div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '10px' }}>
        {currentPage > 0 ? (
          <button className='bubble-button' style={{
            backgroundColor: '#afafaf'
          }} onClick={prevPage}>&lt;</button>
        ) : (
          <div></div> // Empty div for spacing when there's no '<' button
        )}
        <div style={{ marginLeft: 'auto' }}> {/* This ensures '>' is always on the right */}
          {currentPage < pages.length - 1 && <button className='bubble-button' style={{
            backgroundColor: '#afafaf'
          }} onClick={nextPage}>&gt;</button>}
        </div>
      </div>
    </div>
  );
};

export default PagedTextViewer;
