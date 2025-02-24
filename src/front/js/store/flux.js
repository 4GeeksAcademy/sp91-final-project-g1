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
				return data
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
				const data = await response.json()
				return data
			}
		}
	};
};

export default getState;

// Revisar este gist para más detalles sobre la sintaxis dentro del archivo flux.js
// https://gist.github.com/hchocobar/25a43adda3a66130dc2cb2fed8b212d0
