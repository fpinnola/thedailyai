import PagedTextViewer from "./PagedTextViewer";
// import bookmarkFilled from '../assets/bookmark-filled.png'
// import bookmarkEmpty from '../assets/bookmark-empty.png'


const StoryCard = ({ title, summary, url }: { title: string, summary: string, url: string } ) => {

    return (
        <div className="slider-children">
            <div style={{
                justifyContent: 'center',
                alignItems: 'center',
                display: 'flex',
                height: '100%',
                flexDirection: 'column',
                padding: '0px 5px 0px 5px',
            }}>
                <div style={{
                    display: 'flex',
                    flexDirection: 'row',
                    width: '100%',
                    alignItems: 'center',
                    gap: 15,
                    justifyContent: 'center'
                }}>
                    <h4>{title}</h4>
                </div>
                <PagedTextViewer text={summary} charsPerPage={900} />
                <a target="_blank" href={url}>Goto source</a>
            </div>
        </div>
    )

}

export default StoryCard;