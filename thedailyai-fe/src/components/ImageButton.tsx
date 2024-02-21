export default function ImageButton({image, onClick, imageSize }: {image: any, onClick: any ,imageSize: { height: number, width: number }}) {
    return (
        <div onClick={onClick}>
            <img style={{height: imageSize.height, width: imageSize.width}} src={image} />
        </div>
    )
}