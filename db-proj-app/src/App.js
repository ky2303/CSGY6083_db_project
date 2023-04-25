import React, { useState, useEffect } from 'react';

var deployed = false
var localhost = ''

if (deployed){
  localhost = "34.172.159.141"
} else {
  localhost = "localhost"
}

function App() {
  const [data, setData] = useState([]);
  const [newItem, setNewItem] = useState(null);
  const [editing, setEditing] = useState(false);
  const [currentItem, setCurrentItem] = useState({});

  // read items
  useEffect(() => {
    fetch(`http://${localhost}:8000/intel_items/`)
      .then(response => response.json())
      .then(data => setData(data));
  }, []);

  // add new item
  const handleAddItem = () => {
    setNewItem({
      id: data.length+1, // gets screwed up by delete
      name: 'string',
      description: 'string',
      url: 'string',
      comments: 'string',
      date_added: 'string',
      last_updated: 'string',
      GROUPS_id: 0,
      MITIGATIONS_id: 0,
      TACTICS_id: 0,
      TECHNIQUES_id: 0,
      SOFTWARE_id: 0,
      STANDARDS_id: 0,
      image: 'string'
    });
  };

  const handleSaveItem = () => {
    fetch(`http://${localhost}:8000/intel_items/`, {
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

  const handleCancelItem = () => {
    // Clear the new item
    setNewItem(null);
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    setNewItem(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleUpdateItem = (item) => { // need to fix
    //const updateItem = data.find((item) => item.id === id);
    setEditing(true);
    setCurrentItem({ ...item});
  };

  const handleChangeUpdate = (event) => {
    const { name, value } = event.target;
    setCurrentItem(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSaveItemUpdate = () => {
    // Send a PUT request to the API endpoint
    fetch(`http://${localhost}:8000/intel_items/${currentItem.id}`, {
      method: 'PUT', 
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(currentItem)
    })
      .then(response => response.json())
      .then(item => {
        setData(prevState => prevState.map(item => item.id === currentItem.id ? currentItem : item));
      });
      setCurrentItem(null);
      setEditing(false);
  };

  const handleCancelItemUpdate = () => {
    // Clear the new item
    setEditing(false);
  };


  // delete item
  const handleDeleteItem = id => {
    // Send a DELETE request to the API endpoint
    fetch(`http://${localhost}:8000/intel_items/${id}`, { method: 'DELETE' })
      .then(() => {
        // Update the state to remove the deleted item
        setData(prevState => prevState.filter(item => item.id !== id));
      });
  };



  return (
    <>
    <h1>ThreatIntelDB</h1>
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
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {data.map(item => (
            <tr key={item.id}>
              {editing && currentItem.id === item.id ? (
                <>
                <td><input type="text" size="10" defaultValue={item.id} name={"id"} onChange={handleChangeUpdate}/></td>
                <td><input type="text" size="10" defaultValue={item.name} name={"name"} onChange={handleChangeUpdate}/></td>
                <td><input type="text" size="10" defaultValue={item.description} name={"description"} onChange={handleChangeUpdate}/></td>
                <td><input type="text" size="10" defaultValue={item.url} name={"url"} onChange={handleChangeUpdate}/></td>
                <td><input type="text" size="10" defaultValue={item.comments} name={"comments"} onChange={handleChangeUpdate}/></td>
                <td><input type="text" size="10" defaultValue={item.date_added} name={"date_added"} onChange={handleChangeUpdate}/></td>
                <td><input type="text" size="10" defaultValue={item.last_updated} name={"last_updated"} onChange={handleChangeUpdate}/></td>
                <td><input type="text" size="10" defaultValue={item.GROUPS_id} name={"GROUPS_id"} onChange={handleChangeUpdate}/></td>
                <td><input type="text" size="10" defaultValue={item.MITIGATIONS_id} name={"MITIGATIONS_id"} onChange={handleChangeUpdate}/></td>
                <td><input type="text" size="10" defaultValue={item.TACTICS_id} name={"TACTICS_id"} onChange={handleChangeUpdate}/></td>
                <td><input type="text" size="10" defaultValue={item.TECHNIQUES_id} name={"TECHNIQUES_id"} onChange={handleChangeUpdate}/></td>
                <td><input type="text" size="10" defaultValue={item.SOFTWARE_id} name={"SOFTWARE_id"} onChange={handleChangeUpdate}/></td>
                <td><input type="text" size="10" defaultValue={item.STANDARDS_id} name={"STANDARDS_id"} onChange={handleChangeUpdate}/></td>
                <td><input type="text" size="10" defaultValue={item.image} name={"image"} onChange={handleChangeUpdate}/></td>
                <button onClick={handleSaveItemUpdate}>Update</button>
                <button onClick={handleCancelItemUpdate}>Cancel</button>
                </>
              ) : (
                <><td>{item.id}</td>
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
                <button onClick={() => handleUpdateItem(item)}>Edit</button>
                <button onClick={() => handleDeleteItem(item.id)}>Delete</button>
                </>)}
            </tr>
          ))}
          {newItem && (
            <tr>
              {Object.keys(newItem).map(key => (
                <td key={key}>
                  <input
                    type="text"
                    size="10"
                    name={key}
                    value={newItem[key]}
                    onChange={handleChange}
                  />
                </td>
              ))}
              <button onClick={handleSaveItem}>Save</button>
              <button onClick={handleCancelItem}>Cancel</button>
            </tr>
          )}
          <tr><button onClick={handleAddItem}>New</button></tr>
        </tbody>
      </table>
      {/* <div>docs: http://34.172.159.141:8000/docs</div> */}
    </>
  );
}

export default App;