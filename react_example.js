// 🚀 EJEMPLO DE USO DESDE REACT
// Conecta con el servidor Python: truth_detector_server.py

import React, { useEffect, useRef, useState } from 'react';

// ============================================================================
// HOOK PERSONALIZADO PARA WEBSOCKET
// ============================================================================

const useTruthDetector = () => {
	const [isConnected, setIsConnected] = useState(false);
	const [isProcessing, setIsProcessing] = useState(false);
	const [lastResult, setLastResult] = useState(null);
	const [error, setError] = useState(null);
	const [modelInfo, setModelInfo] = useState(null);
	const wsRef = useRef(null);

	const connect = () => {
		try {
			wsRef.current = new WebSocket('ws://localhost:8000/ws');

			wsRef.current.onopen = () => {
				setIsConnected(true);
				setError(null);
				console.log('✅ Conectado al Detector de Verdad');
			};

			wsRef.current.onmessage = (event) => {
				const data = JSON.parse(event.data);
				console.log('📥 Mensaje recibido:', data);

				switch (data.type) {
					case 'welcome':
						setModelInfo(data.model_info);
						break;

					case 'processing':
						setIsProcessing(true);
						break;

					case 'prediction':
						setIsProcessing(false);
						setLastResult(data);
						break;

					case 'batch_prediction':
						setIsProcessing(false);
						setLastResult(data);
						break;

					case 'error':
						setError(data.message);
						setIsProcessing(false);
						break;

					case 'statistics':
						setModelInfo(data.model_statistics);
						break;

					default:
						console.log('Mensaje no reconocido:', data);
				}
			};

			wsRef.current.onerror = (error) => {
				setError('Error de conexión WebSocket');
				setIsConnected(false);
				console.error('❌ Error WebSocket:', error);
			};

			wsRef.current.onclose = () => {
				setIsConnected(false);
				console.log('🔌 Conexión WebSocket cerrada');
			};
		} catch (error) {
			setError('Error al conectar con el servidor');
			console.error('❌ Error conectando:', error);
		}
	};

	const disconnect = () => {
		if (wsRef.current) {
			wsRef.current.close();
			wsRef.current = null;
		}
	};

	const predict = (statement) => {
		if (!isConnected || !wsRef.current) {
			setError('No hay conexión con el servidor');
			return;
		}

		const message = {
			type: 'predict',
			statement: statement,
		};

		wsRef.current.send(JSON.stringify(message));
	};

	const predictBatch = (statements) => {
		if (!isConnected || !wsRef.current) {
			setError('No hay conexión con el servidor');
			return;
		}

		const message = {
			type: 'predict_batch',
			statements: statements,
		};

		wsRef.current.send(JSON.stringify(message));
	};

	const getStatistics = () => {
		if (!isConnected || !wsRef.current) {
			setError('No hay conexión con el servidor');
			return;
		}

		const message = {
			type: 'get_statistics',
		};

		wsRef.current.send(JSON.stringify(message));
	};

	const ping = () => {
		if (!isConnected || !wsRef.current) {
			setError('No hay conexión con el servidor');
			return;
		}

		const message = {
			type: 'ping',
		};

		wsRef.current.send(JSON.stringify(message));
	};

	useEffect(() => {
		// Conectar automáticamente al montar el componente
		connect();

		// Limpiar al desmontar
		return () => {
			disconnect();
		};
	}, []);

	return {
		isConnected,
		isProcessing,
		lastResult,
		error,
		modelInfo,
		predict,
		predictBatch,
		getStatistics,
		ping,
		connect,
		disconnect,
	};
};

// ============================================================================
// COMPONENTE PRINCIPAL
// ============================================================================

const TruthDetectorApp = () => {
	const [statement, setStatement] = useState('');
	const [batchStatements, setBatchStatements] = useState('');

	const {
		isConnected,
		isProcessing,
		lastResult,
		error,
		modelInfo,
		predict,
		predictBatch,
		getStatistics,
		ping,
		connect,
		disconnect,
	} = useTruthDetector();

	const handlePredict = () => {
		if (statement.trim()) {
			predict(statement.trim());
		}
	};

	const handleBatchPredict = () => {
		if (batchStatements.trim()) {
			const statements = batchStatements.split('\n').filter((s) => s.trim());
			if (statements.length > 0) {
				predictBatch(statements);
			}
		}
	};

	return (
		<div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
			<h1>🤖 Detector de Verdad con IA</h1>

			{/* Estado de conexión */}
			<div
				style={{
					padding: '10px',
					margin: '10px 0',
					backgroundColor: isConnected ? '#d4edda' : '#f8d7da',
					border: `1px solid ${isConnected ? '#c3e6cb' : '#f5c6cb'}`,
					borderRadius: '5px',
				}}>
				<strong>Estado:</strong> {isConnected ? '🟢 Conectado' : '🔴 Desconectado'}
				{modelInfo && (
					<div style={{ marginTop: '5px', fontSize: '14px' }}>
						📊 Dataset: {modelInfo.total_statements} afirmaciones | ✅ Verdaderas:{' '}
						{modelInfo.truth_count} | ❌ Falsas: {modelInfo.false_count}
					</div>
				)}
			</div>

			{/* Controles de conexión */}
			<div style={{ margin: '20px 0' }}>
				<button
					onClick={connect}
					disabled={isConnected}
					style={{ marginRight: '10px', padding: '8px 16px' }}>
					🔌 Conectar
				</button>
				<button
					onClick={disconnect}
					disabled={!isConnected}
					style={{ marginRight: '10px', padding: '8px 16px' }}>
					🔌 Desconectar
				</button>
				<button
					onClick={ping}
					disabled={!isConnected}
					style={{ marginRight: '10px', padding: '8px 16px' }}>
					🏓 Ping
				</button>
				<button
					onClick={getStatistics}
					disabled={!isConnected}
					style={{ padding: '8px 16px' }}>
					📊 Estadísticas
				</button>
			</div>

			{/* Predicción individual */}
			<div
				style={{
					margin: '20px 0',
					padding: '20px',
					border: '1px solid #ddd',
					borderRadius: '5px',
				}}>
				<h3>🎯 Predicción Individual</h3>
				<div style={{ marginBottom: '10px' }}>
					<input
						type="text"
						value={statement}
						onChange={(e) => setStatement(e.target.value)}
						placeholder="Escribe una afirmación aquí..."
						style={{ width: '100%', padding: '10px', fontSize: '16px' }}
						disabled={!isConnected || isProcessing}
					/>
				</div>
				<button
					onClick={handlePredict}
					disabled={!isConnected || isProcessing || !statement.trim()}
					style={{ padding: '10px 20px', fontSize: '16px' }}>
					{isProcessing ? '🔄 Analizando...' : '🔍 Analizar'}
				</button>
			</div>

			{/* Predicción por lotes */}
			<div
				style={{
					margin: '20px 0',
					padding: '20px',
					border: '1px solid #ddd',
					borderRadius: '5px',
				}}>
				<h3>🚀 Predicción por Lotes</h3>
				<div style={{ marginBottom: '10px' }}>
					<textarea
						value={batchStatements}
						onChange={(e) => setBatchStatements(e.target.value)}
						placeholder="Escribe una afirmación por línea..."
						rows={4}
						style={{ width: '100%', padding: '10px', fontSize: '16px' }}
						disabled={!isConnected || isProcessing}
					/>
				</div>
				<button
					onClick={handleBatchPredict}
					disabled={!isConnected || isProcessing || !batchStatements.trim()}
					style={{ padding: '10px 20px', fontSize: '16px' }}>
					{isProcessing ? '🔄 Analizando...' : '🔍 Analizar Lote'}
				</button>
			</div>

			{/* Errores */}
			{error && (
				<div
					style={{
						padding: '10px',
						margin: '10px 0',
						backgroundColor: '#f8d7da',
						border: '1px solid #f5c6cb',
						borderRadius: '5px',
						color: '#721c24',
					}}>
					❌ Error: {error}
				</div>
			)}

			{/* Resultados */}
			{lastResult && (
				<div
					style={{
						margin: '20px 0',
						padding: '20px',
						border: '1px solid #ddd',
						borderRadius: '5px',
					}}>
					<h3>📊 Resultado del Análisis</h3>

					{lastResult.type === 'prediction' && (
						<div>
							<p>
								<strong>Afirmación:</strong> "{lastResult.statement}"
							</p>
							<p>
								<strong>Predicción:</strong>
								<span
									style={{
										color:
											lastResult.result.prediction === 'verdadero'
												? 'green'
												: 'red',
										fontWeight: 'bold',
									}}>
									{lastResult.result.prediction === 'verdadero'
										? '✅ Verdadero'
										: '❌ Falso'}
								</span>
							</p>
							<p>
								<strong>Confianza:</strong>{' '}
								{(lastResult.result.confidence * 100).toFixed(1)}% (
								{lastResult.result.confidence_level})
							</p>
							<p>
								<strong>Explicación:</strong> {lastResult.result.explanation}
							</p>
							<p>
								<strong>Similar a:</strong> "
								{lastResult.result.most_similar_statement}"
							</p>
						</div>
					)}

					{lastResult.type === 'batch_prediction' && (
						<div>
							<p>
								<strong>Total analizado:</strong> {lastResult.total_statements}{' '}
								afirmaciones
							</p>
							{lastResult.results.map((item, index) => (
								<div
									key={index}
									style={{
										margin: '10px 0',
										padding: '10px',
										backgroundColor: '#f8f9fa',
										borderRadius: '3px',
									}}>
									<p>
										<strong>{index + 1}.</strong> "{item.statement}" →
										<span
											style={{
												color:
													item.result.prediction === 'verdadero'
														? 'green'
														: 'red',
												fontWeight: 'bold',
											}}>
											{item.result.prediction === 'verdadero'
												? '✅ Verdadero'
												: '❌ Falso'}
										</span>{' '}
										({(item.result.confidence * 100).toFixed(1)}%)
									</p>
								</div>
							))}
						</div>
					)}

					<div style={{ marginTop: '15px', fontSize: '12px', color: '#666' }}>
						<strong>Timestamp:</strong>{' '}
						{new Date(lastResult.timestamp * 1000).toLocaleString()}
					</div>
				</div>
			)}

			{/* Información del modelo */}
			{modelInfo && (
				<div
					style={{
						margin: '20px 0',
						padding: '20px',
						backgroundColor: '#f8f9fa',
						borderRadius: '5px',
					}}>
					<h3>🤖 Información del Modelo</h3>
					<p>
						<strong>Estado:</strong> {modelInfo.status}
					</p>
					<p>
						<strong>Nombre:</strong> {modelInfo.model_name}
					</p>
					<p>
						<strong>Total de afirmaciones:</strong> {modelInfo.total_statements}
					</p>
					<p>
						<strong>Categorías:</strong> {modelInfo.categories.join(', ')}
					</p>
				</div>
			)}
		</div>
	);
};

export default TruthDetectorApp;

// ============================================================================
// USO ALTERNATIVO CON HOOKS SIMPLES
// ============================================================================

// Si prefieres usar hooks más simples, aquí tienes una versión alternativa:

export const useSimpleTruthDetector = () => {
	const [ws, setWs] = useState(null);
	const [isConnected, setIsConnected] = useState(false);

	const connect = () => {
		const websocket = new WebSocket('ws://localhost:8000/ws');

		websocket.onopen = () => {
			setIsConnected(true);
			setWs(websocket);
		};

		websocket.onclose = () => {
			setIsConnected(false);
			setWs(null);
		};

		return websocket;
	};

	const predict = (statement) => {
		if (ws && isConnected) {
			ws.send(
				JSON.stringify({
					type: 'predict',
					statement: statement,
				})
			);
		}
	};

	return { isConnected, connect, predict };
};

// ============================================================================
// EJEMPLO DE USO EN COMPONENTE SIMPLE
// ============================================================================

export const SimpleTruthDetector = () => {
	const { isConnected, connect, predict } = useSimpleTruthDetector();
	const [statement, setStatement] = useState('');

	return (
		<div>
			<h2>Detector Simple</h2>
			<p>Estado: {isConnected ? 'Conectado' : 'Desconectado'}</p>

			{!isConnected && <button onClick={connect}>Conectar</button>}

			{isConnected && (
				<div>
					<input
						value={statement}
						onChange={(e) => setStatement(e.target.value)}
						placeholder="Escribe una afirmación"
					/>
					<button onClick={() => predict(statement)}>Analizar</button>
				</div>
			)}
		</div>
	);
};
