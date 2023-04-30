import { Link } from 'react-router-dom';
import React, { useState, useEffect } from 'react';

var host = 'localhost'
var deployed = true
if (deployed) { host = "127.0.0.1" };

const Home = () => {
	const [data, setData] = useState([]);
  const [newItem, setNewItem] = useState(false);
  const [groups, setGroups] = useState([]);
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [editing, setEditing] = useState(false);
  const [currentItem, setCurrentItem] = useState({});

  // read items
  useEffect(() => {
    fetch(`http://${host}:8000/intel_items/`)
      .then(response => response.json())
      .then(data => setData(data));
  }, []);

  // get groups
  useEffect(() => {
    // Fetch the groups data from the backend
    fetch(`http://${host}:8000/groups/`)
      .then(response => response.json())
      .then(data => setGroups(data));
  }, []);

  // crete a new item
  const handleAddItem = () => {
    const today = new Date();
    console.log(data.map(item => item['id']))
    console.log(Math.max(data.map(item => item['id'])))
    const ids = data.map(item => item['id'])
    var newId = Math.max(...ids)+1
    if (ids.length == 0) { newId = 1 }
    setNewItem({
      id: newId , // gets screwed up by delete
      name: 'string',
      description: 'string',
      url: 'string',
      comments: 'string',
      date_added: new Date(today).toISOString().split('T')[0],
      last_updated: new Date(today).toISOString().split('T')[0],
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
    fetch(`http://${host}:8000/intel_items/`, {
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
    fetch(`http://${host}:8000/intel_items/${currentItem.id}`, {
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
    fetch(`http://${host}:8000/intel_items/${id}`, { method: 'DELETE' })
      .then(() => {
        // Update the state to remove the deleted item
        setData(prevState => prevState.filter(item => item.id !== id));
      });
  };


  return (
    <>
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
                <td><input type="date" size="10" defaultValue={item.date_added} name={"date_added"} onChange={handleChangeUpdate}/></td>
                <td><input type="date" size="10" defaultValue={item.last_updated} name={"last_updated"} onChange={handleChangeUpdate}/></td>
                {/* <td><input type="text" size="10" defaultValue={item.GROUPS_id} name="GROUPS_id" onChange={handleChangeUpdate} /></td> */}
                <td>
                <select value={newItem.GROUPS_id} onChange={handleChange} name={"GROUPS_id"}>
                  {groups.map(group => (
                    <option key={group.id} value={group.id}>
                      {group.name}
                    </option>
                  ))}
                </select>
                </td>
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
                <td><a href={`/groups/${item.GROUPS_id}`}>{item.GROUPS_id}</a></td>
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
            <tr key={newItem.id}>
                <>
                <td><input type="text" size="10" defaultValue={newItem['id']} name={"id"} onChange={handleChange}/></td>
                <td><input type="text" size="10" defaultValue={newItem['name']} name={"name"} onChange={handleChange}/></td>
                <td><input type="text" size="10" defaultValue={newItem['description']} name={"description"} onChange={handleChange}/></td>
                <td><input type="text" size="10" defaultValue={newItem['url']} name={"url"} onChange={handleChange}/></td>
                <td><input type="text" size="10" defaultValue={newItem['comments']} name={"comments"} onChange={handleChange}/></td>
                <td><input type="date" size="10" defaultValue={newItem['date_added']} name={"date_added"} onChange={handleChange}/></td>
                <td><input type="date" size="10" defaultValue={newItem['last_updated']} name={"last_updated"} onChange={handleChange}/></td>
                {/* <td><input type="text" size="10" defaultValue={newItem['GROUPS_id']} name={"GROUPS_id"} onChange={handleChange}/></td> */}
                <td>
                <select value={newItem.GROUPS_id} onChange={handleChange} name={"GROUPS_id"}>
                  {groups.map(group => (
                    <option key={group.id} value={group.id}>
                      {group.name}
                    </option>
                  ))}
                </select>
                </td>
                <td><input type="text" size="10" defaultValue={newItem['MITIGATIONS_id']} name={"MITIGATIONS_id"} onChange={handleChange}/></td>
                <td><input type="text" size="10" defaultValue={newItem['TACTICS_id']} name={"TACTICS_id"} onChange={handleChange}/></td>
                <td><input type="text" size="10" defaultValue={newItem['TECHNIQUES_id']} name={"TECHNIQUES_id"} onChange={handleChange}/></td>
                <td><input type="text" size="10" defaultValue={newItem['SOFTWARE_id']} name={"SOFTWARE_id"} onChange={handleChange}/></td>
                <td><input type="text" size="10" defaultValue={newItem['STANDARDS_id']} name={"STANDARDS_id"} onChange={handleChange}/></td>
                <td><input type="text" size="10" defaultValue={newItem['image']} name={"image"} onChange={handleChange}/></td>
                <button onClick={handleSaveItem}>Save</button>
                <button onClick={handleCancelItem}>Cancel</button>
                </>
              </tr>
          )}
          <tr><button onClick={handleAddItem}>New</button></tr>
        </tbody>
      </table>
    </>
  );
};

export default Home;