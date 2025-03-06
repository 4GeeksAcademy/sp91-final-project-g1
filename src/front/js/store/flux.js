const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			message: null,
		},
		actions: {
			getMessage: async () => {
				const uri = `${process.env.BACKEND_URL}/api/hello`
				const response = await fetch(uri)
				if (!response.ok) {
					console.log("Error loading message from backend", error)
					return
				}
				const data = await response.json()
				setStore({ message: data.message })
				return;
			},
			getFromLocalStorage: (key) => {
				const data = localStorage.getItem(key)
				return JSON.parse(data)
			},
			login: async (dataToSend) => {
				const uri = `${process.env.BACKEND_URL}/api/login`
				const response = await fetch(uri, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify(dataToSend)
				})
				const data = await response.json()
				if (!response.ok) return { status: 400, data: data }
				localStorage.setItem("user", JSON.stringify(data.results))
				localStorage.setItem("accessToken", data.access_token)
				return { status: 200, data: data }
			},
			signup: async (dataToSend) => {
				const uri = `${process.env.BACKEND_URL}/api/users`
				await fetch(uri, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify(dataToSend)
				})
				const body = {
					email: dataToSend.email,
					password: dataToSend.password,
				}
				const loginResponse = await getActions().login(body)
				return loginResponse
			},
			logout: async () => {
				localStorage.clear()
			},
			removeBgFromImage: async (imageUrl) => {
				const url = `${process.env.BACKEND_URL}/api/remove-bg`

				const response = await fetch(url, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({
						image_url: imageUrl
					})
				})

				if (!response.ok) {
					console.error("ERROR AL QUITAR BACKGROUND")
					return "ERROR"
				}
				const data = await response.json()
				return `data:image/png;base64,${data.results}`
			},
			api: {
				get: async (endpoint, extraParams) => {
					const url = `${process.env.BACKEND_URL}/api/${endpoint}${extraParams ? `?${extraParams}` : ''}`

					const response = await fetch(url)

					if(!response.ok) {
						console.error(`Error ${response.status} al llamar a GET /${endpoint}`)
						return
					}
					const data = await response.json()
					return data.results
				},
				post: async (endpoint, body) => {
					const url = `${process.env.BACKEND_URL}/api/${endpoint}`

					const response = await fetch(url, {
						method: 'POST',
						body: JSON.stringify(body)
					})

					if(!response.ok) {
						console.error(`Error ${response.status} al llamar a POST /${endpoint}`)
						return
					}
					const data = await response.json()
					return data.results
				},
				put: async (endpoint, extraParams, body) => {
					const url = `${process.env.BACKEND_URL}/api/${endpoint}${extraParams ? `?${extraParams}` : ''}`

					const response = await fetch(url, {
						method: 'PUT',
						body: JSON.stringify(body)
					})

					if(!response.ok) {
						console.error(`Error ${response.status} al llamar a PUT /${endpoint}${extraParams ? `?${extraParams}` : ''}`)
						return
					}
					const data = await response.json()
					return data.results
				},
				delete: async (endpoint, extraParams) => {
					const url = `${process.env.BACKEND_URL}/api/${endpoint}${extraParams ? `?${extraParams}` : ''}`

					const response = await fetch(url, {
						method: 'DELETE'
					})

					if(!response.ok) {
						console.error(`Error ${response.status} al llamar a DELETE /${endpoint}${extraParams ? `?${extraParams}` : ''}`)
						return
					}
					const data = await response.json()
					return data.results
				},
			},
			updateUser: async (dataToSend) => {
				const uri = `${process.env.BACKEND_URL}/api/update-user`
				const options = {
					method: 'PUT',
					headers: {
						'Content-Type': 'application/json',
						'Authorization': `Bearer ${localStorage.getItem("token")}`
					},
					body: JSON.stringify(dataToSend)
				};
				const response = await fetch(uri, options);

				if (!response.ok) {
					console.error("Error :", response.status, response.statusText);
					return;
				}
				const data = await response.json();
				setStore({ user: data });
			},
			deleteUser: async () => {
				const uri = `${process.env.BACKEND_URL}/api/delete-user`
				const options = {
					method: 'DELETE',
					headers: {
						'Authorization': `Bearer ${localStorage.getItem("token")}`
					},
				};
				const response = await fetch(uri, options);

				if (!response.ok) {
					console.error("Error: ", response.status, response.statusText);
					return;
				}
				localStorage.removeItem("token");
				setStore({ user: null });
			},
			ResetPassword: async (password) => {
				console.log("Contraseña recibida en ResetPassword:", password);
				const uri = `${process.env.BACKEND_URL}/api/reset-password`;
				const options = {
					method: 'PUT',
					headers: {
						'Content-Type': 'application/json',
						'Authorization': `Bearer ${localStorage.getItem("token")}`
					},
					body: JSON.stringify({ password }) 
				};
				const response = await fetch(uri, options);
			
				if (!response.ok) {
					console.error("Error en ResetPassword:", response.status, response.statusText);
					return;
				}
				const data = await response.json();
				console.log(data);
				return;
			},			
		},
	}
};

export default getState;

// Revisar este gist para más detalles sobre la sintaxis dentro del archivo flux.js
// https://gist.github.com/hchocobar/25a43adda3a66130dc2cb2fed8b212d0
