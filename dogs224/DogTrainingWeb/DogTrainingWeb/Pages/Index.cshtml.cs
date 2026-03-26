using DogTrainingApi.Models;
using DogTrainingWeb.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.Threading.Tasks;

namespace DogTrainingWeb.Pages
{
    public class IndexModel : PageModel
    {
        private readonly TrainingService _trainingService;

        public IndexModel(TrainingService trainingService)
        {
            _trainingService = trainingService;
        }

        [BindProperty]
        public TrainingSchedule Schedule { get; set; }

        public string Message { get; set; }
        public bool IsSuccess { get; set; }

        public void OnGet()
        {
            Schedule ??= new TrainingSchedule();
        }

        public async Task<IActionResult> OnPostAsync()
        {
            if (!ModelState.IsValid)
            {
                return Page();
            }

            var result = await _trainingService.SaveTrainingSchedule(Schedule);
            
            if (result)
            {
                Message = "Training schedule saved successfully!";
                IsSuccess = true;
            }
            else
            {
                Message = "Failed to save training schedule. Please try again.";
                IsSuccess = false;
            }

            return Page();
        }
    }
}