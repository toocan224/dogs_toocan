using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using DogTrainingWeb.Models;

namespace DogTrainingWeb.Services
{
    public class TrainingService
    {
        private readonly HttpClient _httpClient;

        public TrainingService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<bool> SaveTrainingSchedule(TrainingSchedule schedule)
        {
            // Теперь просто "api/training", префикс подтянется из BaseAddress
            var response = await _httpClient.PostAsJsonAsync("api/training", schedule);
            return response.IsSuccessStatusCode;
        }

        public async Task<List<TrainingSchedule>> GetAllSchedulesAsync()
        {
            // Теперь это сработает, потому что BaseAddress задан в Program.cs
            return await _httpClient.GetFromJsonAsync<List<TrainingSchedule>>("api/training") 
                ?? new List<TrainingSchedule>();
        }

        public async Task<bool> DeleteScheduleAsync(long id)
        {
            return (await _httpClient.DeleteAsync($"api/training/{id}")).IsSuccessStatusCode;
        }

        public async Task<TrainingSchedule?> GetScheduleByIdAsync(long id)
        {
            return await _httpClient.GetFromJsonAsync<TrainingSchedule>($"api/training/{id}");
        }

        public async Task<bool> UpdateScheduleAsync(long id, TrainingSchedule schedule)
        {
            var response = await _httpClient.PutAsJsonAsync($"api/training/{id}", schedule);
            return response.IsSuccessStatusCode;
        }
    }
}
