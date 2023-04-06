import React, { useState, useEffect } from 'react';

function App() {
  const [data, setData] = useState([]);
  const [newItem, setNewItem] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/intel_items/')
      .then(response => response.json())
      .then(data => setData(data));
  }, []);

  const handleAddItem = () => {
    setNewItem({
      name: '',
      description: '',
      url: '',
      comments: '',
      date_added: '',
      last_updated: '',
      GROUPS_id: '',
      MITIGATIONS_id: '',
      TACTICS_id: '',
      TECHNIQUES_id: '',
      SOFTWARE_id: '',
      STANDARDS_id: '',
      image: ''
    });
  };

  const handleSaveItem = () => {
    fetch('http://localhost:8000/intel_items/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newItem)
    })
      .then(response => response.json())
      .then(item => {
        setData([...data, item]);
        setNewItem(null);
      });
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    setNewItem(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  return (
    <>
      <button onClick={handleAddItem}>+</button>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Description</th>
            <th>URL</th>
            <th>Comments</th>
            <th>Date Added</th>
            <th>Last Updated</th>
            <th>Groups ID</th>
            <th>Mitigations ID</th>
            <th>Tactics ID</th>
            <th>Techniques ID</th>
            <th>Software ID</th>
            <th>Standards ID</th>
            <th>Image</th>
          </tr>
        </thead>
        <tbody>
          {data.map(item => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.name}</td>
              <td>{item.description}</td>
              <td>{item.url}</td>
              <td>{item.comments}</td>
              <td>{item.date_added}</td>
              <td>{item.last_updated}</td>
              <td>{item.GROUPS_id}</td>
              <td>{item.MITIGATIONS_id}</td>
              <td>{item.TACTICS_id}</td>
              <td>{item.TECHNIQUES_id}</td>
              <td>{item.SOFTWARE_id}</td>
              <td>{item.STANDARDS_id}</td>
              <td>{item.image}</td>
            </tr>
          ))}
          {newItem && (
            <tr>
              <td></td>
              {Object.keys(newItem).map(key => (
                <td key={key}>
                  <input
                    type="text"
                    name={key}
                    value={newItem[key]}
                    onChange={handleChange}
                  />
                </td>
              ))}
              <td><button onClick={handleSaveItem}>Save</button></td>
            </tr>
          )}
        </tbody>
      </table>
    </>
  );
}

export default App;