const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			message: null,
			user: null,
		},
		actions: {
			getMessage: async () => {
				const uri = `${process.env.BACKEND_URL}/api/hello`
				const response = await fetch(uri)
				if (!response.ok) {
					console.error("Error loading message from backend", error)
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
				return data.results;
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
				const response = await fetch(uri, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify(dataToSend),
				});

				if (response.ok) {
					const data = await response.json();
					if (data.results) {
						const leagueResponse = await getActions().joinLeague(dataToSend.user_id, dataToSend.fantasy_league_id)
						return true;
					} else {
						return false;
					}
				} else {
					console.error('Error al añadir equipo:', response.statusText);
					return false;
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
				setStore({ user: data.results })
				return response;
			},
			signup: async (dataToSend) => {
				const uri = `${process.env.BACKEND_URL}/api/users`
				const response = await fetch(uri, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify(dataToSend)
				})
				if (!response.ok) {
					return response;
				}
				const body = {
					email: dataToSend.email,
					password: dataToSend.password,
				}
				const loginResponse = await getActions().login(body)
				return loginResponse
			},
			logout: async () => {
				localStorage.clear()
				setStore({ user: null })
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
			},
			updateUser: async (dataToSend) => {
				const uri = `${process.env.BACKEND_URL}/api/update-user`
				const options = {
					method: 'PUT',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${localStorage.getItem("accessToken")}`
					},
					body: JSON.stringify(dataToSend)
				};
				const response = await fetch(uri, options);

				if (!response.ok) {
					console.error("Error :", response.status, response.statusText);
					return response;
				}
				const data = await response.json();
				localStorage.setItem("user", JSON.stringify(data.results))
				return response;
			},
			deleteUser: async () => {
				const uri = `${process.env.BACKEND_URL}/api/delete-user`
				const options = {
					method: 'DELETE',
					headers: {
						Authorization: `Bearer ${localStorage.getItem("accessToken")}`
					},
				};
				const response = await fetch(uri, options);

				if (!response.ok) {
					console.error("Error: ", response.status, response.statusText);
					return;
				}
				localStorage.removeItem("accessToken");
				setStore({ user: null });
			},
			resetPassword: async (dataToSend) => {
				const uri = `${process.env.BACKEND_URL}/api/reset-password`;
				const options = {
					method: 'PUT',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${localStorage.getItem("accessToken")}`
					},
					body: JSON.stringify(dataToSend)
				};
				const response = await fetch(uri, options);

				if (!response.ok) {
					console.error("Error en ResetPassword:", response.status, response.statusText);
					return response;
				}
				const data = await response.json();
				return response;
			},
			getStandings: async () => {
				const standings = await getActions().api.get('standings')
				const teams = await getActions().api.get('teams')
				const data = []
				for (const standing of standings) {
					standing['team'] = teams.find((team) => team.uid === standing.team_id)
					standing['games_played'] = standing['games_won'] + standing['games_draw'] + standing['games_lost']
					standing['goals_diff'] = standing['goals_for'] - standing['goals_against']

					const sortOrder = ['team', 'games_played', 'games_won', 'games_draw', 'games_lost', 'goals_for', 'goals_against', 'goals_diff', 'points', 'form']
					const dataStanding = JSON.parse(JSON.stringify(standing, sortOrder, 4))
					dataStanding['team'] = teams.find((team) => team.uid === standing.team_id)

					data.push(dataStanding)
				}
				return data
			}
		},
	}
};

export default getState;

// Revisar este gist para más detalles sobre la sintaxis dentro del archivo flux.js
// https://gist.github.com/hchocobar/25a43adda3a66130dc2cb2fed8b212d0
