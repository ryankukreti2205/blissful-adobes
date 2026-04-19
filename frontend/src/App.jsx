import { useState } from 'react';

function App() {
  const [guestName, setGuestName] = useState('');
  const [roomType, setRoomType] = useState('Standard Room');
  const [status, setStatus] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleBooking = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setStatus('Processing booking...');

    try {
      const response = await fetch('http://3.89.148.228:5000/book', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          guest_name: guestName,
          room_type: roomType
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setStatus(`Success! Reference ID: ${data.booking_id}`);
        setGuestName('');
      } else {
        setStatus(`Failed: ${data.error}`);
      }
    } catch (error) {
      setStatus('Error connecting to the booking server. Is your EC2 instance running?');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div
      className="min-h-screen relative flex items-center justify-center p-4 bg-cover bg-center"
      style={{
        backgroundImage: "url('https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80')"
      }}
    >
      {/* Global Background Overlay: Darkens and blurs the raw image slightly */}
      <div className="absolute inset-0 bg-black/40 backdrop-blur-sm"></div>

      {/* Floating Form Container: Glassmorphism Effect */}
      <div className="relative z-10 bg-white/85 backdrop-blur-xl p-10 rounded-3xl shadow-[0_20px_50px_rgba(0,_0,_0,_0.5)] border border-white/40 max-w-md w-full">

        <div className="text-center mb-8">
          <h1 className="text-3xl font-light text-gray-900 tracking-wide">
            Blissful Abodes
          </h1>
          <p className="text-sm text-gray-600 mt-2 font-medium tracking-wider uppercase">
            Exclusive Reservations
          </p>
        </div>

        <form onSubmit={handleBooking} className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-gray-800 mb-2">
              Guest Name
            </label>
            <input
              type="text"
              required
              value={guestName}
              onChange={(e) => setGuestName(e.target.value)}
              className="w-full px-4 py-3 bg-white/70 border border-gray-200 rounded-xl focus:ring-2 focus:ring-gray-900 focus:border-transparent focus:outline-none transition-all"
              placeholder="Enter full name"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-800 mb-2">
              Room Type
            </label>
            <div className="relative">
              <select
                value={roomType}
                onChange={(e) => setRoomType(e.target.value)}
                className="w-full px-4 py-3 bg-white/70 border border-gray-200 rounded-xl focus:ring-2 focus:ring-gray-900 focus:border-transparent focus:outline-none appearance-none transition-all cursor-pointer"
              >
                <option value="Standard Room">Standard Room</option>
                <option value="Deluxe Suite">Deluxe Suite</option>
                <option value="Presidential Suite">Presidential Suite</option>
              </select>
              {/* Custom dropdown arrow for a cleaner look */}
              <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-gray-700">
                <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" /></svg>
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-gray-900 text-white font-medium py-3.5 rounded-xl hover:bg-gray-800 transition-all transform hover:-translate-y-0.5 shadow-lg disabled:bg-gray-400 disabled:transform-none disabled:shadow-none mt-4"
          >
            {isLoading ? 'Confirming...' : 'Complete Booking'}
          </button>
        </form>

        {/* Dynamic Status Message */}
        {status && (
          <div className={`mt-6 p-4 rounded-xl text-sm text-center font-medium transition-all ${status.includes('Success') ? 'bg-green-100/90 text-green-800 border border-green-200' : 'bg-red-100/90 text-red-800 border border-red-200'}`}>
            {status}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;