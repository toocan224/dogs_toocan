using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using DogTrainingWeb.Models;
using DogTrainingWeb.Services;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace DogTrainingWeb.Pages
{
    public class ManageModel : PageModel
    {
        private readonly TrainingService _service;
        public List<TrainingSchedule> Schedules { get; set; } = new();

        public ManageModel(TrainingService service) => _service = service;

        public async Task OnGetAsync()
        {
            Schedules = await _service.GetAllSchedulesAsync();
        }

        public async Task<IActionResult> OnPostDeleteAsync(long id)
        {
            await _service.DeleteScheduleAsync(id);
            return RedirectToPage();
        }
    }
}

