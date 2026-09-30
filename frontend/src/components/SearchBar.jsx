export default function SearchBar({

    value,

    onChange

}) {

    return (

        <input

            className="search-box"

            placeholder="Search..."

            value={value}

            onChange={onChange}

        />

    );

}