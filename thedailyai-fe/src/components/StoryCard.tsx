import PagedTextViewer from "./PagedTextViewer";
import QuestionInput from "./QuestionInput";


const StoryCard = ({ title, summary }: { title: string, summary: string } ) => {

    const truncateText = (inputText: string) => {
        if (inputText.length > 500) {
          return `${inputText.substring(0, 500)}...`;
        }
        return inputText;
    };

    return (
        <div className="slider-children">
            <div style={{
                justifyContent: 'center',
                alignItems: 'center',
                display: 'flex',
                height: '100%',
                flexDirection: 'column',
                padding: '5px 5px 10px 10px'
            }}>
                <h4>{title}</h4>
                <PagedTextViewer text={summary} charsPerPage={1000} />
                {/* <p>{truncateText(summary)}</p> */}
                {/* <QuestionInput /> */}
                {/* <button style={{
                    backgroundColor: '#afafaf'
                 }}>Read more</button> */}
            </div>
        </div>
    )

}

export default StoryCard;