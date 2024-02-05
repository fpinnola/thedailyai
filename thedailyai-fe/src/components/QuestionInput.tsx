
export default function QuestionInput() {
    return (
        <div className="searchInputContainer">
            <input
            type="text"
            // value={inputValue}
            // onChange={handleInputChange}
            className="searchInput"
            placeholder="Ask a question..."
            />
            <button className="searchButton">
            Go
            </button>
        </div>
    )
}