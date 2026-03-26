using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using DogTrainingApi.Models;

namespace DogTrainingWeb.Services
{
    public class TrainingService
    {
        private readonly HttpClient _httpClient;
        private readonly string _apiBaseUrl = "http://localhost:5159/api/training"; // Замените на IP вашей Raspberry Pi

        public TrainingService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<bool> SaveTrainingSchedule(TrainingSchedule schedule)
        {
            var json = JsonSerializer.Serialize(schedule);
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            var response = await _httpClient.PostAsync(_apiBaseUrl, content);
            return response.IsSuccessStatusCode;
        }
    }
}