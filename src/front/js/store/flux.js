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
			getUserTeam: async (id) => {
				const uri = `${process.env.BACKEND_URL}/api/users/${id}/fantasy-teams`
				const response = await fetch(uri)
				if (!response.ok) {
					return null
				}
				const data = await response.json()
				return data;
			},
			getUserLeague: async () => {
				const uri = `${process.env.BACKEND_URL}/api/fantasy-league`
				const response = await fetch(uri)
				if (!response.ok) {
					return
				}
				const data = await response.json()
				return data;
			},
			joinLeague: async (userId, leagueId) => {
				const uri = `${process.env.BACKEND_URL}/api/users/${userId}/join-league/${leagueId}`
				const response = await fetch(uri, {
					method: 'POST',
				})
				if (response.ok) {
					return true;
				} else {
					console.error("Error al unirse a la liga", response.statusText);
					return false;
				}
			},
			addUser: async (dataToSend) => {
				const uri = `${process.env.BACKEND_URL}/api/fantatsy-league-teams`
				const body = {
					fantasy_team_id: dataToSend.fantasy_team_id,
					fantasy_league_id: dataToSend.fantasy_league_id,
				}
				const response = await fetch(uri, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify(body)
				})
				const user = await response.json()
				return user
			},
			addTeam: async (dataToSend) => {
				const uri = `${process.env.BACKEND_URL}/api/fantasy-teams`; 
				const body = {
					user_id: dataToSend.user_id,  
					name: dataToSend.name,       
					logo: dataToSend.logo,       
				};
				const response = await fetch(uri, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json', 
					},
					body: JSON.stringify(body), 
				});
			
				if (response.ok) {
					const data = await response.json(); 
					if (data.results) {
						return true;
					} else {	
						return false;
					}
				} else {
					console.error('Error al añadir equipo:', response.statusText);	
					return false;
				}
			},
			getUserTeam: async() =>{
				const response = await fetch('/api/fantasy-team', {
					method: 'GET',
					headers: {
						'Content-Type': 'application/json',
					},
				});
				if (response.ok) {
					const data = await response.json();
					if (data.team) {
						setUserHasTeam(true); 
					} else {
						setUserHasTeam(false);
					}
				} else {
					console.error('Error al obtener los datos del equipo del usuario');
				}
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

					if (!response.ok) {
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

					if (!response.ok) {
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

					if (!response.ok) {
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

					if (!response.ok) {
						console.error(`Error ${response.status} al llamar a DELETE /${endpoint}${extraParams ? `?${extraParams}` : ''}`)
						return
					}
					const data = await response.json()
					return data.results
				},
			}
		}
	};
}
	export default getState;

// Revisar este gist para más detalles sobre la sintaxis dentro del archivo flux.js
// https://gist.github.com/hchocobar/25a43adda3a66130dc2cb2fed8b212d0
