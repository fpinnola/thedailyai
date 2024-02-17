import './CategoryLabel.css';

const stringToColor = (str: string) => {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 2) - hash);
  }
  const color = `hsla(${hash % 360}, 100%, 50%, 0.2)`; // Using HSLA for color and fixed 50% transparency
  return color;
}

const CategoryLabel = ({ label }: { label: string }) => {
  const backgroundColor = stringToColor(label);
  return (
    <div className="category-label" style={{ backgroundColor }}>
      {label}
    </div>
  );
};

export default CategoryLabel;
