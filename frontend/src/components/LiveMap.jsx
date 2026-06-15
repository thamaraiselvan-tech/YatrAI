// src/components/LiveMap.jsx
import { useEffect, useRef, useState, useCallback } from 'react'
import { MapPin, Crosshair, Layers, Search, X } from 'lucide-react'

const CATEGORY_ICONS = {
  station: '🚉',
  temple: '🛕',
  mall: '🏬',
  hospital: '🏥',
  landmark: '🏛️',
}

const CATEGORY_COLORS = {
  station: '#B45309',
  temple: '#7C3AED',
  mall: '#0369A1',
  hospital: '#EF4444',
  landmark: '#0F766E',
}

const MODE_COLORS = {
  Suburban_Train: '#B45309',
  Metro: '#7C3AED',
  MTC_Bus: '#0369A1',
  SETC_Bus: '#0369A1',
  Town_Bus: '#0369A1',
  Walk: '#6B7280',
  Rapido_Bike: '#0F766E',
  Ola_Auto: '#B45309',
  Intercity_Train: '#B45309',
}

export default function LiveMap({ position, route, expanded, onToggle, onPlaceSelect, isDarkMode }) {
  const mapRef = useRef(null)
  const mapInstanceRef = useRef(null)
  const markersLayerRef = useRef(null)
  const routeLayerRef = useRef(null)
  const userMarkerRef = useRef(null)
  const userAccuracyCircleRef = useRef(null)
  const hasCenteredRef = useRef(false)
  const [places, setPlaces] = useState([])
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [searching, setSearching] = useState(false)
  const [selectedCategory, setSelectedCategory] = useState('')
  const [showSearch, setShowSearch] = useState(false)
  const [mapStyle, setMapStyle] = useState('street') // 'street' or 'satellite'

  // Initialize Leaflet map
  useEffect(() => {
    if (!mapRef.current || mapInstanceRef.current) return
    if (!window.L) return

    const map = window.L.map(mapRef.current, {
      center: [13.0827, 80.2707], // Chennai Central
      zoom: 12,
      zoomControl: false,
      attributionControl: false,
    })

    // Add zoom control to bottom right
    window.L.control.zoom({ position: 'bottomright' }).addTo(map)

    // Marker layer group
    markersLayerRef.current = window.L.layerGroup().addTo(map)
    routeLayerRef.current = window.L.layerGroup().addTo(map)

    mapInstanceRef.current = map

    // Fetch all places
    fetch('/api/coordinates')
      .then(r => r.json())
      .then(data => {
        setPlaces(data.coordinates || [])
        addPlaceMarkers(data.coordinates || [], map)
      })
      .catch(() => {})

    // Force Leaflet to recalculate bounds after initial mount
    setTimeout(() => {
      map.invalidateSize()
    }, 150)

    return () => {
      map.remove()
      mapInstanceRef.current = null
    }
  }, [])

  // Dynamic high-quality modern tile switching (with auto dark/light theme styling)
  useEffect(() => {
    if (!mapInstanceRef.current) return
    const map = mapInstanceRef.current

    if (map._activeTileLayer) {
      map.removeLayer(map._activeTileLayer)
    }

    let url
    let attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'

    if (mapStyle === 'satellite') {
      url = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
      attribution = 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
    } else {
      // Apply luxury dark/light vector-like styles
      if (isDarkMode) {
        url = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
      } else {
        url = 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png'
      }
    }

    const layer = window.L.tileLayer(url, {
      maxZoom: 20,
      attribution,
    }).addTo(map)

    map._activeTileLayer = layer
  }, [mapStyle, isDarkMode])

  // Dynamic layout correction: invalidate Leaflet map size during container transition
  useEffect(() => {
    if (!mapInstanceRef.current) return
    mapInstanceRef.current.invalidateSize()

    // Periodically invalidate map size during transition animation (duration-300)
    const interval = setInterval(() => {
      mapInstanceRef.current?.invalidateSize()
    }, 50)

    const timer = setTimeout(() => {
      clearInterval(interval)
      mapInstanceRef.current?.invalidateSize()
    }, 350)

    return () => {
      clearInterval(interval)
      clearTimeout(timer)
    }
  }, [expanded])

  // Add place markers to map
  function addPlaceMarkers(placeList, map) {
    if (!markersLayerRef.current) return
    markersLayerRef.current.clearLayers()

    placeList.forEach(p => {
      if (selectedCategory && p.category !== selectedCategory) return

      const icon = window.L.divIcon({
        className: '',
        html: `<div style="
          font-size: 16px; width: 28px; height: 28px;
          display: flex; align-items: center; justify-content: center;
          background: ${CATEGORY_COLORS[p.category] || '#64748B'}22;
          border: 2px solid ${CATEGORY_COLORS[p.category] || '#64748B'};
          border-radius: 50%; cursor: pointer;
        ">${CATEGORY_ICONS[p.category] || '📍'}</div>`,
        iconSize: [28, 28],
        iconAnchor: [14, 14],
      })

      const marker = window.L.marker([p.lat, p.lng], { icon })
      marker.bindPopup(`
        <div style="font-family: 'Inter', sans-serif; min-width: 150px; color: #0F172A;">
          <strong style="font-size: 13px; font-weight: 600;">${p.name}</strong>
          <br><span style="font-size: 12px; color: #4B5563;">${p.city} · ${p.category}</span>
        </div>
      `)
      marker.on('click', () => {
        if (onPlaceSelect) onPlaceSelect(p)
      })
      markersLayerRef.current.addLayer(marker)
    })
  }

  // Update markers when category filter changes
  useEffect(() => {
    if (!mapInstanceRef.current || places.length === 0) return
    addPlaceMarkers(places, mapInstanceRef.current)
  }, [selectedCategory, places])

  // Update user position marker and draw live accuracy circle around user position
  useEffect(() => {
    if (!mapInstanceRef.current || !position) return
    const map = mapInstanceRef.current
    const latlng = [position.lat, position.lng]

    if (userMarkerRef.current) {
      userMarkerRef.current.setLatLng(latlng)
    } else {
      const icon = window.L.divIcon({
        className: '',
        html: `<div style="
          width: 18px; height: 18px;
          background: #3B82F6;
          border: 3px solid white;
          border-radius: 50%;
          box-shadow: 0 0 12px rgba(59,130,246,0.6), 0 0 24px rgba(59,130,246,0.3);
          animation: pulse 2s infinite;
        "></div>
        <style>@keyframes pulse { 0%,100% { box-shadow: 0 0 12px rgba(59,130,246,0.6); } 50% { box-shadow: 0 0 24px rgba(59,130,246,0.9); } }</style>`,
        iconSize: [18, 18],
        iconAnchor: [9, 9],
      })
      userMarkerRef.current = window.L.marker(latlng, { icon, zIndexOffset: 1000 })
      userMarkerRef.current.addTo(map)
    }

    // Add accuracy radius circle around the user (e.g. blue ring showing live GPS resolution)
    if (position.accuracy) {
      if (userAccuracyCircleRef.current) {
        userAccuracyCircleRef.current.setLatLng(latlng)
        userAccuracyCircleRef.current.setRadius(position.accuracy)
      } else {
        userAccuracyCircleRef.current = window.L.circle(latlng, {
          radius: position.accuracy,
          color: '#3B82F6',
          fillColor: '#3B82F6',
          fillOpacity: 0.12,
          weight: 1.5,
        }).addTo(map)
      }
    } else {
      if (userAccuracyCircleRef.current) {
        map.removeLayer(userAccuracyCircleRef.current)
        userAccuracyCircleRef.current = null
      }
    }

    // On first location load, auto-center map around the user's live position
    if (!hasCenteredRef.current) {
      map.setView(latlng, 15, { animate: true })
      hasCenteredRef.current = true
    }
  }, [position])

  // Draw route on map
  useEffect(() => {
    if (!mapInstanceRef.current || !routeLayerRef.current) return
    routeLayerRef.current.clearLayers()

    if (!route?.segments?.length) return
    const map = mapInstanceRef.current

    // Import coordinates from places data
    const coordMap = {}
    places.forEach(p => { coordMap[p.node] = [p.lat, p.lng] })

    const allPoints = []
    route.segments.forEach(seg => {
      const from = coordMap[seg.from_node]
      const to = coordMap[seg.to_node]
      if (!from || !to) return

      allPoints.push(from, to)
      const color = MODE_COLORS[seg.mode] || '#3B82F6'
      const line = window.L.polyline([from, to], {
        color,
        weight: 4,
        opacity: 0.8,
        dashArray: seg.mode === 'Walk' ? '8, 8' : null,
      })
      routeLayerRef.current.addLayer(line)

      // Start/end markers
      const startIcon = window.L.divIcon({
        className: '',
        html: `<div style="width:10px;height:10px;background:${color};border:2px solid white;border-radius:50%;"></div>`,
        iconSize: [10, 10],
        iconAnchor: [5, 5],
      })
      routeLayerRef.current.addLayer(window.L.marker(from, { icon: startIcon }))
      routeLayerRef.current.addLayer(window.L.marker(to, { icon: startIcon }))
    })

    if (allPoints.length > 0) {
      map.fitBounds(allPoints, { padding: [40, 40] })
    }
  }, [route, places])

  // Recenter on user
  const recenter = useCallback(() => {
    if (!mapInstanceRef.current || !position) return
    mapInstanceRef.current.setView([position.lat, position.lng], 15, { animate: true })
  }, [position])

  // Toggle map style
  const toggleStyle = useCallback(() => {
    setMapStyle(prev => prev === 'street' ? 'satellite' : 'street')
  }, [])

  // Search places
  const handleSearch = useCallback(async (q) => {
    setSearchQuery(q)
    if (!q.trim()) {
      setSearchResults([])
      return
    }
    setSearching(true)
    try {
      const r = await fetch(`/api/places?q=${encodeURIComponent(q)}&limit=8`)
      const data = await r.json()
      setSearchResults(data.places || [])
    } catch { setSearchResults([]) }
    setSearching(false)
  }, [])

  const handleSelectResult = useCallback((place) => {
    if (!mapInstanceRef.current) return
    mapInstanceRef.current.setView([place.lat, place.lng], 16, { animate: true })
    setShowSearch(false)
    setSearchQuery('')
    setSearchResults([])
    if (onPlaceSelect) onPlaceSelect(place)
  }, [onPlaceSelect])

  const categories = [
    { id: '', label: 'All', icon: '📍' },
    { id: 'station', label: 'Stations', icon: '🚉' },
    { id: 'temple', label: 'Temples', icon: '🛕' },
    { id: 'mall', label: 'Malls', icon: '🏬' },
    { id: 'hospital', label: 'Hospitals', icon: '🏥' },
    { id: 'landmark', label: 'Landmarks', icon: '🏛️' },
  ]

  return (
    <div className={`relative rounded-2xl overflow-hidden border border-white/10 transition-all duration-300 ${expanded ? 'h-[70vh]' : 'h-[200px]'}`}>
      {/* Map Container */}
      <div ref={mapRef} className="w-full h-full" style={{ background: '#031427' }} />

      {/* Search Bar */}
      {showSearch && (
        <div className="absolute top-3 left-3 right-3 z-[1000]">
          <div className="glass-panel rounded-[14px] flex flex-col shadow-lg overflow-hidden">
            <div className="flex items-center gap-3 px-4 h-[52px]">
              <Search size={18} className="text-[#3B82F6] shrink-0" />
              <input
                autoFocus
                value={searchQuery}
                onChange={(e) => handleSearch(e.target.value)}
                placeholder="Search temples, malls, stations..."
                className="flex-1 bg-transparent text-[13px] text-slate-800 dark:text-white outline-none placeholder-slate-400"
              />
              <button 
                onClick={() => { setShowSearch(false); setSearchResults([]) }} 
                className="w-11 h-11 flex items-center justify-center text-slate-400 hover:text-slate-600 dark:hover:text-white shrink-0"
              >
                <X size={18} />
              </button>
            </div>
            {searchResults.length > 0 && (
              <div className="max-h-48 overflow-y-auto border-t border-black/[0.05] dark:border-white/[0.05]">
                {searchResults.map(p => (
                  <button
                    key={p.node}
                    onClick={() => handleSelectResult(p)}
                    className="w-full text-left px-4 py-3 hover:bg-slate-50 dark:hover:bg-slate-800 flex items-center gap-3 transition-colors border-b border-black/[0.03] dark:border-white/[0.03] last:border-0"
                  >
                    <span className="text-sm">{CATEGORY_ICONS[p.category] || '📍'}</span>
                    <div className="flex flex-col gap-0.5">
                      <p className="text-xs text-[#0F172A] dark:text-white font-medium">{p.name}</p>
                      <p className="text-[12px] text-slate-400">{p.city} · {p.area}</p>
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Category Filter Chips */}
      <div className="absolute top-3 left-3 right-[60px] z-[999] flex gap-1.5 overflow-x-auto no-scrollbar"
           style={{ display: showSearch ? 'none' : 'flex' }}>
        {categories.map(c => (
          <button
            key={c.id}
            onClick={() => setSelectedCategory(c.id)}
            className={`flex items-center gap-1.5 h-11 px-3.5 rounded-full text-[12px] font-semibold whitespace-nowrap transition-all
              ${selectedCategory === c.id
                ? 'bg-[#3B82F6] text-white shadow-md'
                : 'glass-panel text-slate-600 dark:text-slate-300 hover:text-[#3B82F6] dark:hover:text-[#3B82F6]'}`}
          >
            <span>{c.icon}</span> {c.label}
          </button>
        ))}
      </div>

      {/* Floating Controls */}
      <div className="absolute right-3 top-3 z-[999] flex flex-col gap-2">
        <button
          onClick={() => setShowSearch(true)}
          className="w-11 h-11 rounded-xl glass-panel flex items-center justify-center text-[#3B82F6] hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors shadow-md"
          title="Search"
        >
          <Search size={18} />
        </button>
      </div>

      <div className="absolute right-3 bottom-20 z-[999] flex flex-col gap-2">
        <button
          onClick={recenter}
          className="w-11 h-11 rounded-xl glass-panel flex items-center justify-center text-[#3B82F6] hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors shadow-md"
          title="Recenter"
        >
          <Crosshair size={18} />
        </button>
        <button
          onClick={toggleStyle}
          className="w-11 h-11 rounded-xl glass-panel flex items-center justify-center text-[#3B82F6] hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors shadow-md"
          title="Toggle map style"
        >
          <Layers size={18} />
        </button>
      </div>

      {/* Expand/Collapse toggle */}
      <button
        onClick={onToggle}
        className="absolute bottom-3 left-1/2 -translate-x-1/2 z-[999] glass-panel rounded-full h-11 px-5 flex items-center justify-center
                   text-[12px] font-semibold text-[#3B82F6] hover:bg-slate-100 dark:hover:bg-slate-800 transition-all shadow-md"
      >
        {expanded ? '▼ Collapse Map' : '▲ Expand Map'}
      </button>
    </div>
  )
}
